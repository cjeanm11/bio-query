from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Final, Tuple

@dataclass
class RabbitNode:
    name: str
    parents: Tuple['RabbitNode']

# version 1
def getCommonAncestors(rabbit_node_1: RabbitNode, rabbit_node_2: RabbitNode):
    max_limit_generation: Final = 4
    ancestors_set_1 = set()
    ancestors_set_2 = set()
    
    while rabbit_node_1:
        ancestors_set_1.add(rabbit_node_1)
        rabbit_node_1 = rabbit_node_1.parents[0] if rabbit_node_1.parents[0] # Assume one parent for simplicity
    
    while rabbit_node_2:
        ancestors_set_2.add(rabbit_node_2)
        rabbit_node_2 = rabbit_node_2.parents[0] if rabbit_node_2.parents[0] 
        
    return ancestors_set_1 & ancestors_set_2
    
    
    
# version 2
def getCommonAncestors_2(rabbit_node_1: RabbitNode, rabbit_node_2: RabbitNode):
    max_limit_generation: Final = 4 # max limit of generation
    ancestors_set_1 = set()
    generation_index = 0
    
    while rabbit_node_1 and generation_index < max_limit_generation:
        
        if rabbit_node_1 == rabbit_node_2: # fast return
            return True
            
        ancestors_set_1.add(rabbit_node_1)
        rabbit_node_1 = rabbit_node_1.parents[0] if rabbit_node_1.parents[0] # Assume one parent for simplicity
        generation_index += 1
    
    generation_index = 0
    while rabbit_node_2 and  generation_index < max_limit_generation:
        
        if rabbit_node_2 in ancestors_set_1: # fast return 
            return True
            
        rabbit_node_2 = rabbit_node_2.parents[0] if rabbit_node_2.parents[0] 
        generation_index += 1
        
    return False 
