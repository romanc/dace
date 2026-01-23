import dace 
from dace.properties import CodeBlock
from dace.sdfg.state import ConditionalBlock, ControlFlowRegion, LoopRegion

def for_loop_example() -> dace.SDFG:
    sdfg = dace.SDFG("for_loop_example")
    state0 = sdfg.add_state('state0', is_start_block=True)

    loop1 = LoopRegion(label='loop1', condition_expr='i < 10', loop_var='i', initialize_expr='i = 0',
                       update_expr='i = i + 1', inverted=False)
    sdfg.add_node(loop1)
    sdfg.add_symbol('i', dace.int32)
    sdfg.add_array('A', [10], dace.float32)

    state1 = loop1.add_state('state1', is_start_block=True)
    acc_a = state1.add_access('A')
    t1 = state1.add_tasklet('t1', None, {'a'}, 'a = i')
    state1.add_edge(t1, 'a', acc_a, None, dace.Memlet('A[i]'))
    
    state3 = sdfg.add_state('state3')
    sdfg.add_edge(state0, loop1, dace.InterstateEdge())
    sdfg.add_edge(loop1, state3, dace.InterstateEdge())

    return sdfg

def if_scope_example() -> dace.SDFG:
    sdfg = dace.SDFG("if_scope_example")
    state0 = sdfg.add_state("state0", is_start_block=True)

    sdfg.add_array("A", [10], dace.float32)

    if_block = ConditionalBlock("conditional1")
    sdfg.add_node(if_block)
    sdfg.add_edge(state0, if_block, dace.InterstateEdge())

    if_body = ControlFlowRegion("if_body", sdfg=sdfg)
    if_body.add_state("if_state", is_start_block=True)
    elif_body = ControlFlowRegion("elif_body", sdfg=sdfg)
    elif_body.add_state("elif_state", is_start_block=True)
    else_body = ControlFlowRegion("else_body", sdfg=sdfg)
    else_body.add_state("else_state", is_start_block=True)

    if_block.add_branch(CodeBlock("A[0] > 0"), if_body)
    if_block.add_branch(CodeBlock("A[0] == 0"), elif_body)
    if_block.add_branch(None, else_body)

    after_state = sdfg.add_state("after_state")
    sdfg.add_edge(if_block, after_state, dace.InterstateEdge())

    return sdfg

def map_scope_example() -> dace.SDFG:
    sdfg = dace.SDFG("map_scope_example")

    return sdfg


if __name__ == "__main__":
    sdfg = for_loop_example()
    sdfg.validate()

    sdfg2 = if_scope_example()
    sdfg2.validate()

    # same as before?
    sdfg3 = map_scope_example()
    sdfg3.validate()

    assert True