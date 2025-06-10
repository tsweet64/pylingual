from typing import override
from ..cft import ControlFlowTemplate, EdgeKind, register_template
from ..utils import T, N, exact_instructions, starting_instructions, to_indented_source, make_try_match, versions_from

class WithCleanup3_11(ControlFlowTemplate):
    template = T(
        start=N("reraise", "poptop", "exc").with_cond(
            starting_instructions("PUSH_EXC_INFO", "WITH_EXCEPT_START"),  # 3.11 and later
        ),
        reraise=N(None, None, "exc").with_cond(exact_instructions("RERAISE")).with_in_deg(1),
        poptop=N("tail", None, "exc").with_cond(exact_instructions("POP_TOP")).with_in_deg(1),
        exc=+N().with_cond(exact_instructions("COPY", "POP_EXCEPT", "RERAISE")).with_in_deg(3),
        tail=~N.tail().with_cond(starting_instructions("POP_EXCEPT", "POP_TOP", "POP_TOP")).with_in_deg(1),
    )

    try_match = make_try_match({}, "start", "reraise", "poptop", "exc", "tail")

    @to_indented_source
    def to_indented_source(self, source):
        """
        {tail}
        """

@register_template(0, 10, (3, 11), (3, 12), (3, 13))
class With3_11(ControlFlowTemplate):
    template = T(
        setup_with=~N("with_body", None),
        with_body=N("normal_cleanup.", None, "exc_cleanup").with_in_deg(1),
        exc_cleanup=N.tail().of_subtemplate(WithCleanup3_11).with_in_deg(1),
        normal_cleanup=~N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "normal_cleanup"}, "setup_with", "with_body", "exc_cleanup")

    @to_indented_source
    def to_indented_source():
        """
        {setup_with}
            {with_body}
        {exc_cleanup}
        """