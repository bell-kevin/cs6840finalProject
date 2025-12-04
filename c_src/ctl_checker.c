#define _POSIX_C_SOURCE 200809L

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LABEL_LEN 64

// -------------------- data structures --------------------
typedef struct {
    int from;
    int to;
} Transition;

typedef struct {
    int num_states;
    int num_transitions;
    Transition *transitions;
    char ***labeling;        // labeling[state][label_index]
    int *label_counts;       // number of labels per state
    int init_count;
    int *init_states;
} TransitionSystem;

typedef struct {
    int size;
    unsigned char *data; // 0/1 membership
} StateSet;

typedef enum {
    NODE_ATOM,
    NODE_NOT,
    NODE_AND,
    NODE_OR,
    NODE_EX,
    NODE_AX,
    NODE_EF,
    NODE_AF,
    NODE_EG,
    NODE_AG,
    NODE_EU,
    NODE_AU
} NodeType;

typedef struct Node {
    NodeType type;
    char *atom;
    struct Node *left;
    struct Node *right;
} Node;

// -------------------- memory helpers --------------------
static void *checked_calloc(size_t count, size_t size) {
    void *ptr = calloc(count, size);
    if (!ptr) {
        fprintf(stderr, "Out of memory\n");
        exit(EXIT_FAILURE);
    }
    return ptr;
}

static char *checked_strdup(const char *src) {
    char *copy = strdup(src);
    if (!copy) {
        fprintf(stderr, "Out of memory\n");
        exit(EXIT_FAILURE);
    }
    return copy;
}

// -------------------- set operations --------------------
static StateSet set_create(int size) {
    StateSet s;
    s.size = size;
    s.data = (unsigned char *)checked_calloc(size, sizeof(unsigned char));
    return s;
}

static void set_free(StateSet *s) {
    free(s->data);
    s->data = NULL;
    s->size = 0;
}

static bool set_equal(const StateSet *a, const StateSet *b) {
    if (a->size != b->size) return false;
    return memcmp(a->data, b->data, a->size) == 0;
}

static StateSet set_union(const StateSet *a, const StateSet *b) {
    StateSet res = set_create(a->size);
    for (int i = 0; i < a->size; i++) {
        res.data[i] = (unsigned char)((a->data[i] || b->data[i]) ? 1 : 0);
    }
    return res;
}

static StateSet set_intersection(const StateSet *a, const StateSet *b) {
    StateSet res = set_create(a->size);
    for (int i = 0; i < a->size; i++) {
        res.data[i] = (unsigned char)((a->data[i] && b->data[i]) ? 1 : 0);
    }
    return res;
}

static StateSet set_complement(const StateSet *a) {
    StateSet res = set_create(a->size);
    for (int i = 0; i < a->size; i++) {
        res.data[i] = (unsigned char)(a->data[i] ? 0 : 1);
    }
    return res;
}

// -------------------- transition system helpers --------------------
static int has_label(const TransitionSystem *ts, int state, const char *label) {
    for (int i = 0; i < ts->label_counts[state]; i++) {
        if (strcmp(ts->labeling[state][i], label) == 0) {
            return 1;
        }
    }
    return 0;
}

static StateSet pre(const TransitionSystem *ts, const StateSet *X) {
    StateSet res = set_create(ts->num_states);
    for (int i = 0; i < ts->num_transitions; i++) {
        int u = ts->transitions[i].from;
        int v = ts->transitions[i].to;
        if (X->data[v]) {
            res.data[u] = 1;
        }
    }
    return res;
}

// -------------------- parser --------------------
typedef enum {
    TOK_EOF,
    TOK_IDENTIFIER,
    TOK_NOT,
    TOK_AND,
    TOK_OR,
    TOK_EX,
    TOK_AX,
    TOK_EF,
    TOK_AF,
    TOK_EG,
    TOK_AG,
    TOK_E,
    TOK_A,
    TOK_U,
    TOK_LPAREN,
    TOK_RPAREN,
    TOK_LBRACKET,
    TOK_RBRACKET
} TokenType;

typedef struct {
    TokenType type;
    char lexeme[MAX_LABEL_LEN];
} Token;

typedef struct {
    Token *tokens;
    int count;
    int pos;
} TokenStream;

static int is_identifier_char(int c) {
    return isalnum(c) || c == '_';
}

static TokenStream tokenize(const char *input) {
    TokenStream stream;
    stream.tokens = (Token *)checked_calloc(strlen(input) + 2, sizeof(Token));
    stream.count = 0;
    stream.pos = 0;

    const char *p = input;
    while (*p) {
        if (isspace((unsigned char)*p)) {
            p++;
            continue;
        }
        if (*p == '(') {
            stream.tokens[stream.count++] = (Token){TOK_LPAREN, "("};
            p++;
            continue;
        }
        if (*p == ')') {
            stream.tokens[stream.count++] = (Token){TOK_RPAREN, ")"};
            p++;
            continue;
        }
        if (*p == '[') {
            stream.tokens[stream.count++] = (Token){TOK_LBRACKET, "["};
            p++;
            continue;
        }
        if (*p == ']') {
            stream.tokens[stream.count++] = (Token){TOK_RBRACKET, "]"};
            p++;
            continue;
        }

        if (is_identifier_char(*p)) {
            char buf[MAX_LABEL_LEN];
            int idx = 0;
            while (*p && is_identifier_char(*p) && idx < MAX_LABEL_LEN - 1) {
                buf[idx++] = (char)*p;
                p++;
            }
            buf[idx] = '\0';
            Token tok;
            tok.type = TOK_IDENTIFIER;
            strncpy(tok.lexeme, buf, MAX_LABEL_LEN);

            if (strcmp(buf, "NOT") == 0) tok.type = TOK_NOT;
            else if (strcmp(buf, "AND") == 0) tok.type = TOK_AND;
            else if (strcmp(buf, "OR") == 0) tok.type = TOK_OR;
            else if (strcmp(buf, "EX") == 0) tok.type = TOK_EX;
            else if (strcmp(buf, "AX") == 0) tok.type = TOK_AX;
            else if (strcmp(buf, "EF") == 0) tok.type = TOK_EF;
            else if (strcmp(buf, "AF") == 0) tok.type = TOK_AF;
            else if (strcmp(buf, "EG") == 0) tok.type = TOK_EG;
            else if (strcmp(buf, "AG") == 0) tok.type = TOK_AG;
            else if (strcmp(buf, "E") == 0) tok.type = TOK_E;
            else if (strcmp(buf, "A") == 0) tok.type = TOK_A;
            else if (strcmp(buf, "U") == 0) tok.type = TOK_U;

            stream.tokens[stream.count++] = tok;
            continue;
        }

        fprintf(stderr, "Unexpected character in formula: %c\n", *p);
        exit(EXIT_FAILURE);
    }
    stream.tokens[stream.count++] = (Token){TOK_EOF, ""};
    return stream;
}

static Token current_token(TokenStream *stream) {
    return stream->tokens[stream->pos];
}

static Token advance(TokenStream *stream) {
    return stream->tokens[stream->pos++];
}

static void expect(TokenStream *stream, TokenType type, const char *message) {
    if (current_token(stream).type != type) {
        fprintf(stderr, "Parse error: %s\n", message);
        exit(EXIT_FAILURE);
    }
    advance(stream);
}

static Node *parse_expr(TokenStream *stream);

static Node *make_node(NodeType type, Node *left, Node *right, const char *atom) {
    Node *node = (Node *)checked_calloc(1, sizeof(Node));
    node->type = type;
    node->left = left;
    node->right = right;
    if (atom) node->atom = checked_strdup(atom);
    return node;
}

static Node *parse_unary(TokenStream *stream);

static Node *parse_paren(TokenStream *stream) {
    expect(stream, TOK_LPAREN, "Expected '('");
    Node *node = parse_expr(stream);
    expect(stream, TOK_RPAREN, "Expected ')'");
    return node;
}

static Node *parse_until(TokenStream *stream, bool universal) {
    advance(stream); // consume E or A
    expect(stream, TOK_LBRACKET, "Expected '[' after path quantifier");
    Node *left = parse_expr(stream);
    expect(stream, TOK_U, "Expected 'U' in until expression");
    Node *right = parse_expr(stream);
    expect(stream, TOK_RBRACKET, "Expected ']' after until expression");
    return make_node(universal ? NODE_AU : NODE_EU, left, right, NULL);
}

static Node *parse_unary(TokenStream *stream) {
    Token tok = current_token(stream);
    switch (tok.type) {
        case TOK_NOT:
            advance(stream);
            return make_node(NODE_NOT, parse_unary(stream), NULL, NULL);
        case TOK_EX:
            advance(stream);
            return make_node(NODE_EX, parse_unary(stream), NULL, NULL);
        case TOK_AX:
            advance(stream);
            return make_node(NODE_AX, parse_unary(stream), NULL, NULL);
        case TOK_EF:
            advance(stream);
            return make_node(NODE_EF, parse_unary(stream), NULL, NULL);
        case TOK_AF:
            advance(stream);
            return make_node(NODE_AF, parse_unary(stream), NULL, NULL);
        case TOK_EG:
            advance(stream);
            return make_node(NODE_EG, parse_unary(stream), NULL, NULL);
        case TOK_AG:
            advance(stream);
            return make_node(NODE_AG, parse_unary(stream), NULL, NULL);
        case TOK_E:
            return parse_until(stream, false);
        case TOK_A:
            return parse_until(stream, true);
        case TOK_LPAREN:
            return parse_paren(stream);
        case TOK_IDENTIFIER: {
            advance(stream);
            return make_node(NODE_ATOM, NULL, NULL, tok.lexeme);
        }
        default:
            fprintf(stderr, "Unexpected token while parsing\n");
            exit(EXIT_FAILURE);
    }
}

static Node *parse_and(TokenStream *stream) {
    Node *node = parse_unary(stream);
    while (current_token(stream).type == TOK_AND) {
        advance(stream);
        node = make_node(NODE_AND, node, parse_unary(stream), NULL);
    }
    return node;
}

static Node *parse_or(TokenStream *stream) {
    Node *node = parse_and(stream);
    while (current_token(stream).type == TOK_OR) {
        advance(stream);
        node = make_node(NODE_OR, node, parse_and(stream), NULL);
    }
    return node;
}

static Node *parse_expr(TokenStream *stream) {
    return parse_or(stream);
}

static Node *parse_ctl(const char *input) {
    TokenStream stream = tokenize(input);
    Node *root = parse_expr(&stream);
    if (current_token(&stream).type != TOK_EOF) {
        fprintf(stderr, "Unexpected input after end of formula\n");
        exit(EXIT_FAILURE);
    }
    free(stream.tokens);
    return root;
}

static void free_ast(Node *node) {
    if (!node) return;
    free_ast(node->left);
    free_ast(node->right);
    free(node->atom);
    free(node);
}

// -------------------- CTL evaluation --------------------
static StateSet eval(const TransitionSystem *ts, Node *node) {
    switch (node->type) {
        case NODE_ATOM: {
            StateSet res = set_create(ts->num_states);
            for (int s = 0; s < ts->num_states; s++) {
                if (has_label(ts, s, node->atom)) res.data[s] = 1;
            }
            return res;
        }
        case NODE_NOT: {
            StateSet child = eval(ts, node->left);
            StateSet res = set_complement(&child);
            set_free(&child);
            return res;
        }
        case NODE_AND: {
            StateSet left = eval(ts, node->left);
            StateSet right = eval(ts, node->right);
            StateSet res = set_intersection(&left, &right);
            set_free(&left);
            set_free(&right);
            return res;
        }
        case NODE_OR: {
            StateSet left = eval(ts, node->left);
            StateSet right = eval(ts, node->right);
            StateSet res = set_union(&left, &right);
            set_free(&left);
            set_free(&right);
            return res;
        }
        case NODE_EX: {
            StateSet child = eval(ts, node->left);
            StateSet res = pre(ts, &child);
            set_free(&child);
            return res;
        }
        case NODE_AX: {
            StateSet child = eval(ts, node->left);
            StateSet not_child = set_complement(&child);
            StateSet pre_not = pre(ts, &not_child);
            StateSet res = set_complement(&pre_not);
            set_free(&child);
            set_free(&not_child);
            set_free(&pre_not);
            return res;
        }
        case NODE_EF: {
            StateSet child = eval(ts, node->left);
            StateSet Y = set_create(ts->num_states);
            while (1) {
                StateSet preY = pre(ts, &Y);
                StateSet candidate = set_union(&child, &preY);
                if (set_equal(&candidate, &Y)) {
                    set_free(&preY);
                    set_free(&child);
                    set_free(&Y);
                    return candidate;
                }
                set_free(&preY);
                set_free(&Y);
                Y = candidate;
            }
        }
        case NODE_AF: {
            StateSet child = eval(ts, node->left);
            StateSet Y = set_create(ts->num_states);
            while (1) {
                StateSet notY = set_complement(&Y);
                StateSet pre_not = pre(ts, &notY);
                StateSet not_pre_not = set_complement(&pre_not);
                StateSet candidate = set_union(&child, &not_pre_not);
                set_free(&notY);
                set_free(&pre_not);
                set_free(&not_pre_not);
                if (set_equal(&candidate, &Y)) {
                    set_free(&child);
                    set_free(&Y);
                    return candidate;
                }
                set_free(&Y);
                Y = candidate;
            }
        }
        case NODE_EG: {
            StateSet child = eval(ts, node->left);
            StateSet Y = set_create(ts->num_states);
            for (int i = 0; i < ts->num_states; i++) Y.data[i] = 1;
            while (1) {
                StateSet preY = pre(ts, &Y);
                StateSet candidate = set_intersection(&child, &preY);
                if (set_equal(&candidate, &Y)) {
                    set_free(&preY);
                    set_free(&child);
                    set_free(&Y);
                    return candidate;
                }
                set_free(&preY);
                set_free(&Y);
                Y = candidate;
            }
        }
        case NODE_AG: {
            StateSet child = eval(ts, node->left);
            StateSet Y = set_create(ts->num_states);
            for (int i = 0; i < ts->num_states; i++) Y.data[i] = 1;
            while (1) {
                StateSet notY = set_complement(&Y);
                StateSet pre_not = pre(ts, &notY);
                StateSet not_pre_not = set_complement(&pre_not);
                StateSet candidate = set_intersection(&child, &not_pre_not);
                set_free(&notY);
                set_free(&pre_not);
                set_free(&not_pre_not);
                if (set_equal(&candidate, &Y)) {
                    set_free(&child);
                    set_free(&Y);
                    return candidate;
                }
                set_free(&Y);
                Y = candidate;
            }
        }
        case NODE_EU: {
            StateSet phi = eval(ts, node->left);
            StateSet psi = eval(ts, node->right);
            StateSet Y = set_create(ts->num_states);
            while (1) {
                StateSet preY = pre(ts, &Y);
                StateSet inter = set_intersection(&phi, &preY);
                StateSet candidate = set_union(&psi, &inter);
                set_free(&preY);
                set_free(&inter);
                if (set_equal(&candidate, &Y)) {
                    set_free(&phi);
                    set_free(&psi);
                    set_free(&Y);
                    return candidate;
                }
                set_free(&Y);
                Y = candidate;
            }
        }
        case NODE_AU: {
            StateSet phi = eval(ts, node->left);
            StateSet psi = eval(ts, node->right);
            StateSet Y = set_create(ts->num_states);
            while (1) {
                StateSet notY = set_complement(&Y);
                StateSet pre_not = pre(ts, &notY);
                StateSet not_pre_not = set_complement(&pre_not);
                StateSet inter = set_intersection(&phi, &not_pre_not);
                StateSet candidate = set_union(&psi, &inter);
                set_free(&notY);
                set_free(&pre_not);
                set_free(&not_pre_not);
                set_free(&inter);
                if (set_equal(&candidate, &Y)) {
                    set_free(&phi);
                    set_free(&psi);
                    set_free(&Y);
                    return candidate;
                }
                set_free(&Y);
                Y = candidate;
            }
        }
    }
    fprintf(stderr, "Unknown node type encountered\n");
    exit(EXIT_FAILURE);
}

static bool satisfies(const TransitionSystem *ts, Node *ast) {
    StateSet result = eval(ts, ast);
    bool ok = true;
    for (int i = 0; i < ts->init_count; i++) {
        int s = ts->init_states[i];
        if (s < 0 || s >= ts->num_states || !result.data[s]) {
            ok = false;
            break;
        }
    }
    set_free(&result);
    return ok;
}

// -------------------- input parsing --------------------
static void free_transition_system(TransitionSystem *ts) {
    if (!ts) return;
    for (int s = 0; s < ts->num_states; s++) {
        for (int i = 0; i < ts->label_counts[s]; i++) {
            free(ts->labeling[s][i]);
        }
        free(ts->labeling[s]);
    }
    free(ts->labeling);
    free(ts->label_counts);
    free(ts->init_states);
    free(ts->transitions);
}

static void load_transition_system(const char *path, TransitionSystem *ts, char **formula_out) {
    FILE *f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "Could not open input file %s\n", path);
        exit(EXIT_FAILURE);
    }

    if (fscanf(f, "states %d\n", &ts->num_states) != 1) {
        fprintf(stderr, "Expected 'states <n>' line\n");
        exit(EXIT_FAILURE);
    }

    ts->labeling = (char ***)checked_calloc(ts->num_states, sizeof(char **));
    ts->label_counts = (int *)checked_calloc(ts->num_states, sizeof(int));

    if (fscanf(f, "init %d", &ts->init_count) != 1) {
        fprintf(stderr, "Expected 'init <k>' line\n");
        exit(EXIT_FAILURE);
    }
    ts->init_states = (int *)checked_calloc(ts->init_count, sizeof(int));
    for (int i = 0; i < ts->init_count; i++) {
        if (fscanf(f, "%d", &ts->init_states[i]) != 1) {
            fprintf(stderr, "Failed to read init state index\n");
            exit(EXIT_FAILURE);
        }
    }

    if (fscanf(f, "\ntransitions %d\n", &ts->num_transitions) != 1) {
        fprintf(stderr, "Expected 'transitions <m>' line\n");
        exit(EXIT_FAILURE);
    }
    ts->transitions = (Transition *)checked_calloc(ts->num_transitions, sizeof(Transition));
    for (int i = 0; i < ts->num_transitions; i++) {
        if (fscanf(f, "%d %d", &ts->transitions[i].from, &ts->transitions[i].to) != 2) {
            fprintf(stderr, "Failed to read transition pair\n");
            exit(EXIT_FAILURE);
        }
    }

    int label_lines = 0;
    if (fscanf(f, "\nlabels %d", &label_lines) != 1) {
        fprintf(stderr, "Expected 'labels <n>' line\n");
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < label_lines; i++) {
        int state, count;
        if (fscanf(f, "%d %d", &state, &count) != 2) {
            fprintf(stderr, "Failed to read label header\n");
            exit(EXIT_FAILURE);
        }
        ts->label_counts[state] = count;
        ts->labeling[state] = (char **)checked_calloc(count, sizeof(char *));
        for (int j = 0; j < count; j++) {
            char buf[MAX_LABEL_LEN];
            if (fscanf(f, "%63s", buf) != 1) {
                fprintf(stderr, "Failed to read label string\n");
                exit(EXIT_FAILURE);
            }
            ts->labeling[state][j] = checked_strdup(buf);
        }
    }

    int c;
    while ((c = fgetc(f)) != '\n' && c != EOF) {
        // skip rest of line
    }

    char formula_buf[512];
    if (!fgets(formula_buf, sizeof(formula_buf), f)) {
        fprintf(stderr, "Expected formula line\n");
        exit(EXIT_FAILURE);
    }
    size_t len = strlen(formula_buf);
    if (len > 0 && formula_buf[len - 1] == '\n') {
        formula_buf[len - 1] = '\0';
    }
    *formula_out = checked_strdup(formula_buf);
    fclose(f);
}

// -------------------- main --------------------
int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return EXIT_FAILURE;
    }

    TransitionSystem ts = {0};
    char *formula = NULL;
    load_transition_system(argv[1], &ts, &formula);

    Node *ast = parse_ctl(formula);
    bool result = satisfies(&ts, ast);

    printf(result ? "true\n" : "false\n");

    free_ast(ast);
    free(formula);
    free_transition_system(&ts);
    return result ? EXIT_SUCCESS : EXIT_FAILURE;
}

