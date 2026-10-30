from string import Template

MOD_REORDERED_PROMPT = Template("""
<problem-description>
You are a highly-skilled professor in AI planning and a proficient Python programmer creating a domain-dependent heuristic function for the PDDL domain <domain>$name</domain>. The heuristic function you create will be used to guide a greedy best-first search to solve instances from this domain. Therefore, the heuristic does not need to be admissible. For a given state, the heuristic function should estimate the required number of actions to reach a goal state as accurately as possible, while remaining efficiently computable. The name of the heuristic should be $heuristic_name. The heuristic should be efficiently computable, and it should minimize the number of expanded nodes during the search. Next, you will receive a sequence of file contents to help you with your task and to show you the definition of the $name domain.
</problem-description>

This is the PDDL domain file of the $name domain, for which you need to create a domain-dependent heuristic:
<domain-file>
$domain
</domain-file>

This is an example of a PDDL instance file of the $name domain:
<instance-file-example-1>
$instance1
</instance-file-example-1>

This is a second example of a PDDL instance file of the $name domain:
<instance-file-example-2>
$instance2
</instance-file-example-2>

This is the PDDL domain file of another domain, called Ferry, which serves as an example:
<ferry-domain-file>
(define (domain ferry)

	(:requirements :strips)
	(:predicates
		(not-eq ?x ?y)
		(at-ferry ?l)
		(at ?c ?l)
		(empty-ferry)
		(on ?c)
		(car ?c)
		(location ?l)
	)

	(:action sail
		:parameters (?from ?to)
		:precondition (and
			(location ?from)
			(location ?to)
			(at-ferry ?from)
			(not-eq ?from ?to)
		)
		:effect (and
			(at-ferry ?to)
			(not (at-ferry ?from))
		)
	)
	(:action board
		:parameters (?car ?loc)
		:precondition (and
			(car ?car)
			(location ?loc)
			(at ?car ?loc)
			(at-ferry ?loc)
			(empty-ferry)
		)
		:effect (and
			(on ?car)
			(not (at ?car ?loc))
			(not (empty-ferry))
		)
	)
	(:action debark
		:parameters (?car ?loc)
		:precondition (and
			(car ?car)
			(location ?loc)
			(on ?car)
			(at-ferry ?loc)
		)
		:effect (and
			(at ?car ?loc)
			(empty-ferry)
			(not (on ?car))
		)
	)
)
 
</ferry-domain-file>

This is an example of an instance file from the Ferry domain:
<ferry-instance-file-example>
(define (problem ferry-50)
(:domain ferry)
(:objects
	car1 car2 car3 car4 car5 car6 car7 car8 car9 loc1 loc2 loc3 loc4 loc5 loc6 loc7 loc8 loc9
)

(:init
	(at car1 loc7)
	(at car2 loc9)
	(at car3 loc7)
	(at car4 loc6)
	(at car5 loc6)
	(at car6 loc9)
	(at car7 loc7)
	(at car8 loc6)
	(at car9 loc1)
	(at-ferry loc5)
	(car car1)
	(car car2)
	(car car3)
	(car car4)
	(car car5)
	(car car6)
	(car car7)
	(car car8)
	(car car9)
	(empty-ferry)
	(location loc1)
	(location loc2)
	(location loc3)
	(location loc4)
	(location loc5)
	(location loc6)
	(location loc7)
	(location loc8)
	(location loc9)
	(not-eq loc1 loc2)
	(not-eq loc1 loc3)
	(not-eq loc1 loc4)
	(not-eq loc1 loc5)
	(not-eq loc1 loc6)
	(not-eq loc1 loc7)
	(not-eq loc1 loc8)
	(not-eq loc1 loc9)
	(not-eq loc2 loc1)
	(not-eq loc2 loc3)
	(not-eq loc2 loc4)
	(not-eq loc2 loc5)
	(not-eq loc2 loc6)
	(not-eq loc2 loc7)
	(not-eq loc2 loc8)
	(not-eq loc2 loc9)
	(not-eq loc3 loc1)
	(not-eq loc3 loc2)
	(not-eq loc3 loc4)
	(not-eq loc3 loc5)
	(not-eq loc3 loc6)
	(not-eq loc3 loc7)
	(not-eq loc3 loc8)
	(not-eq loc3 loc9)
	(not-eq loc4 loc1)
	(not-eq loc4 loc2)
	(not-eq loc4 loc3)
	(not-eq loc4 loc5)
	(not-eq loc4 loc6)
	(not-eq loc4 loc7)
	(not-eq loc4 loc8)
	(not-eq loc4 loc9)
	(not-eq loc5 loc1)
	(not-eq loc5 loc2)
	(not-eq loc5 loc3)
	(not-eq loc5 loc4)
	(not-eq loc5 loc6)
	(not-eq loc5 loc7)
	(not-eq loc5 loc8)
	(not-eq loc5 loc9)
	(not-eq loc6 loc1)
	(not-eq loc6 loc2)
	(not-eq loc6 loc3)
	(not-eq loc6 loc4)
	(not-eq loc6 loc5)
	(not-eq loc6 loc7)
	(not-eq loc6 loc8)
	(not-eq loc6 loc9)
	(not-eq loc7 loc1)
	(not-eq loc7 loc2)
	(not-eq loc7 loc3)
	(not-eq loc7 loc4)
	(not-eq loc7 loc5)
	(not-eq loc7 loc6)
	(not-eq loc7 loc8)
	(not-eq loc7 loc9)
	(not-eq loc8 loc1)
	(not-eq loc8 loc2)
	(not-eq loc8 loc3)
	(not-eq loc8 loc4)
	(not-eq loc8 loc5)
	(not-eq loc8 loc6)
	(not-eq loc8 loc7)
	(not-eq loc8 loc9)
	(not-eq loc9 loc1)
	(not-eq loc9 loc2)
	(not-eq loc9 loc3)
	(not-eq loc9 loc4)
	(not-eq loc9 loc5)
	(not-eq loc9 loc6)
	(not-eq loc9 loc7)
	(not-eq loc9 loc8)
)

(:goal
(and
	(at car1 loc8)
	(at car2 loc4)
	(at car3 loc1)
	(at car4 loc8)
	(at car5 loc4)
	(at car6 loc3)
	(at car7 loc1)
	(at car8 loc3)
	(at car9 loc9)
))
)
</ferry-instance-file-example>

This is an example of a domain-dependent heuristic for Ferry:
<code-file-heuristic-1>
$heuristic1
</code-file-heuristic-1>

This is the PDDL domain file of another domain, called Grid, to serve as a second example:
<grid-domain-file>
(define (domain grid)
(:requirements :strips)
(:predicates (conn ?x ?y)
             (key-shape ?k ?s)
             (lock-shape ?x ?s)
             (at ?r ?x )
	     (at-robot ?x)
             (place ?p)
             (key ?k)
             (shape ?s)
             (locked ?x)
             (holding ?k)
             (open ?x)
             (arm-empty ))



(:action unlock
:parameters (?curpos ?lockpos ?key ?shape)
:precondition (and (place ?curpos) (place ?lockpos) (key ?key) (shape ?shape)
          (conn ?curpos ?lockpos) (key-shape ?key ?shape)
                   (lock-shape ?lockpos ?shape) (at-robot ?curpos) 
                   (locked ?lockpos) (holding ?key))
:effect (and  (open ?lockpos) (not (locked ?lockpos))))


(:action move
:parameters (?curpos ?nextpos)
:precondition (and (place ?curpos) (place ?nextpos)
               (at-robot ?curpos) (conn ?curpos ?nextpos) (open ?nextpos))
:effect (and (at-robot ?nextpos) (not (at-robot ?curpos))))

(:action pickup
:parameters (?curpos ?key)
:precondition (and (place ?curpos) (key ?key) 
                  (at-robot ?curpos) (at ?key ?curpos) (arm-empty ))
:effect (and (holding ?key)
   (not (at ?key ?curpos)) (not (arm-empty ))))


(:action pickup-and-loose
:parameters (?curpos ?newkey ?oldkey)
:precondition (and (place ?curpos) (key ?newkey) (key ?oldkey)
                  (at-robot ?curpos) (holding ?oldkey) (at ?newkey ?curpos))
:effect (and (holding ?newkey) (at ?oldkey ?curpos)
        (not (holding ?oldkey)) (not (at ?newkey ?curpos))))

(:action putdown
:parameters (?curpos ?key)
:precondition (and (place ?curpos) (key ?key) 
                  (at-robot ?curpos) (holding ?key))
:effect (and (arm-empty ) (at ?key ?curpos) (not (holding ?key)))))
</grid-domain-file>

This is an example of an instance file from the Grid domain:
<grid-instance-file-example>
(define (problem grid-3-2-1-2-1)
    (:domain grid)
    (:objects
    pos0-0 pos0-1 pos1-0 pos1-1 pos2-0 pos2-1
    shape0
    key0 key1
    )

    (:init
       (arm-empty)

       (place pos0-0)
       (place pos0-1)
       (place pos1-0)
       (place pos1-1)
       (place pos2-0)
       (place pos2-1)
       (shape shape0)
       (key key0)
       (key key1)

       (conn pos0-0 pos1-0)
       (conn pos0-0 pos0-1)
       (conn pos0-1 pos1-1)
       (conn pos0-1 pos0-0)
       (conn pos1-0 pos2-0)
       (conn pos1-0 pos1-1)
       (conn pos1-0 pos0-0)
       (conn pos1-1 pos2-1)
       (conn pos1-1 pos0-1)
       (conn pos1-1 pos1-0)
       (conn pos2-0 pos2-1)
       (conn pos2-0 pos1-0)
       (conn pos2-1 pos1-1)
       (conn pos2-1 pos2-0)
       (locked pos1-0)
       (lock-shape  pos1-0 shape0)
       (open pos0-0)
       (open pos0-1)
       (open pos1-1)
       (open pos2-0)
       (open pos2-1)

       (key-shape  key0 shape0)
       (key-shape  key1 shape0)
       (at key0 pos2-1)
       (at key1 pos2-1)
       (at-robot pos1-1)
    )

    (:goal (and
       (at key1 pos2-0)
    ))) 
</grid-instance-file-example>

This is an example of a domain-dependent heuristic for Grid:
<code-file-heuristic-2>
$heuristic2
</code-file-heuristic-2>

This is how an example state from the $name domain is represented internally by the planner. Note that PDDL facts are represented as strings, for example '(predicate_name object1 object2)'.
<state>
$state
</state>

This is an example for how the static information is represented internally by the planner:
<static>
$static
</static>

This is the source code for representing operators and tasks in the planner:
<code-file-task>
$task
</code-file-task>

Provide only the Python code, inside a code block using triple backticks, of the domain-dependent heuristic for the $name domain. Here is a checklist to help you with your code:
1) The code for extracting objects from facts remembers to ignore the surrounding brackets.
2) The heuristic is 0 only for goal states.
3) The heuristic value is finite for solvable states.
4) All used modules are imported.
5) The information from static facts is extracted into suitable data structures in the constructor.
6) Provide a detailed docstring explaining the heuristic calculation. For this, divide the docstring into sections "Summary", "Assumptions", "Heuristic Initialization" and "Step-By-Step Thinking for Computing Heuristic".
""")
