#define _POSIX_C_SOURCE 200809L

#include <assert.h>
#include <stdio.h>

#include "ctl_checker.c"

static TransitionSystem make_simple_ts(void) {
    TransitionSystem ts = {0};
    ts.num_states = 2;
    ts.init_count = 1;
    ts.num_transitions = 2;

    ts.labeling = (char ***)checked_calloc(ts.num_states, sizeof(char **));
    ts.label_counts = (int *)checked_calloc(ts.num_states, sizeof(int));
    ts.init_states = (int *)checked_calloc(ts.init_count, sizeof(int));
    ts.init_states[0] = 0;

    ts.transitions = (Transition *)checked_calloc(ts.num_transitions, sizeof(Transition));
    ts.transitions[0] = (Transition){0, 1};
    ts.transitions[1] = (Transition){1, 1};

    ts.label_counts[0] = 1;
    ts.labeling[0] = (char **)checked_calloc(1, sizeof(char *));
    ts.labeling[0][0] = checked_strdup("q");

    ts.label_counts[1] = 1;
    ts.labeling[1] = (char **)checked_calloc(1, sizeof(char *));
    ts.labeling[1][0] = checked_strdup("p");

    return ts;
}

static TransitionSystem make_linear_ts(void) {
    TransitionSystem ts = {0};
    ts.num_states = 3;
    ts.init_count = 1;
    ts.num_transitions = 3;

    ts.labeling = (char ***)checked_calloc(ts.num_states, sizeof(char **));
    ts.label_counts = (int *)checked_calloc(ts.num_states, sizeof(int));
    ts.init_states = (int *)checked_calloc(ts.init_count, sizeof(int));
    ts.init_states[0] = 0;

    ts.transitions = (Transition *)checked_calloc(ts.num_transitions, sizeof(Transition));
    ts.transitions[0] = (Transition){0, 1};
    ts.transitions[1] = (Transition){1, 2};
    ts.transitions[2] = (Transition){2, 2};

    ts.label_counts[0] = 1;
    ts.labeling[0] = (char **)checked_calloc(1, sizeof(char *));
    ts.labeling[0][0] = checked_strdup("p");

    ts.label_counts[1] = 1;
    ts.labeling[1] = (char **)checked_calloc(1, sizeof(char *));
    ts.labeling[1][0] = checked_strdup("p");

    ts.label_counts[2] = 1;
    ts.labeling[2] = (char **)checked_calloc(1, sizeof(char *));
    ts.labeling[2][0] = checked_strdup("r");

    return ts;
}

static TransitionSystem make_two_init_ts(void) {
    TransitionSystem ts = {0};
    ts.num_states = 2;
    ts.init_count = 2;
    ts.num_transitions = 2;

    ts.labeling = (char ***)checked_calloc(ts.num_states, sizeof(char **));
    ts.label_counts = (int *)checked_calloc(ts.num_states, sizeof(int));
    ts.init_states = (int *)checked_calloc(ts.init_count, sizeof(int));
    ts.init_states[0] = 0;
    ts.init_states[1] = 1;

    ts.transitions = (Transition *)checked_calloc(ts.num_transitions, sizeof(Transition));
    ts.transitions[0] = (Transition){0, 0};
    ts.transitions[1] = (Transition){1, 1};

    ts.label_counts[0] = 1;
    ts.labeling[0] = (char **)checked_calloc(1, sizeof(char *));
    ts.labeling[0][0] = checked_strdup("p");

    ts.label_counts[1] = 0;
    ts.labeling[1] = NULL;

    return ts;
}

static void test_set_complement(void) {
    StateSet s = set_create(3);
    s.data[0] = 1;
    s.data[2] = 1;

    StateSet comp = set_complement(&s);
    assert(comp.size == 3);
    assert(comp.data[0] == 0);
    assert(comp.data[1] == 1);
    assert(comp.data[2] == 0);

    set_free(&s);
    set_free(&comp);
}

static void test_predecessor_operator(void) {
    TransitionSystem ts = make_simple_ts();
    StateSet target = set_create(ts.num_states);
    target.data[1] = 1;

    StateSet pre_image = pre(&ts, &target);
    assert(pre_image.data[0] == 1);
    assert(pre_image.data[1] == 1);

    set_free(&target);
    set_free(&pre_image);
    free_transition_system(&ts);
}

static void test_satisfies_af_true(void) {
    TransitionSystem ts = make_simple_ts();
    Node *ast = parse_ctl("AF p");

    assert(satisfies(&ts, ast) == true);

    free_ast(ast);
    free_transition_system(&ts);
}

static void test_satisfies_ag_false(void) {
    TransitionSystem ts = make_simple_ts();
    Node *ast = parse_ctl("AG p");

    assert(satisfies(&ts, ast) == false);

    free_ast(ast);
    free_transition_system(&ts);
}

static void test_satisfies_eu_true(void) {
    TransitionSystem ts = make_linear_ts();
    Node *ast = parse_ctl("E[p U r]");

    assert(satisfies(&ts, ast) == true);

    free_ast(ast);
    free_transition_system(&ts);
}

static void test_satisfies_au_true(void) {
    TransitionSystem ts = make_linear_ts();
    Node *ast = parse_ctl("A[p U r]");

    assert(satisfies(&ts, ast) == true);

    free_ast(ast);
    free_transition_system(&ts);
}

static void test_multiple_inits_must_satisfy(void) {
    TransitionSystem ts = make_two_init_ts();
    Node *ast = parse_ctl("p");

    assert(satisfies(&ts, ast) == false);

    free_ast(ast);
    free_transition_system(&ts);
}

int main(void) {
    struct {
        const char *name;
        void (*fn)(void);
    } tests[] = {
        {"set complement", test_set_complement},
        {"predecessor operator", test_predecessor_operator},
        {"AF holds", test_satisfies_af_true},
        {"AG falsified", test_satisfies_ag_false},
        {"E until holds", test_satisfies_eu_true},
        {"A until holds", test_satisfies_au_true},
        {"all init states required", test_multiple_inits_must_satisfy},
    };

    for (size_t i = 0; i < sizeof(tests) / sizeof(tests[0]); i++) {
        tests[i].fn();
        printf("[pass] %s\n", tests[i].name);
    }

    printf("All C unit tests passed.\n");
    return 0;
}

