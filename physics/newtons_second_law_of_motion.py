"""
Description :
Newton's second law of motion pertains to the behavior of objects for which
all existing forces are not balanced.
The second law of motion states that the force acting on a body is directly proportional to the rate of change of momentum of the object.

But when we consider the mass of the body as constant, then, the acceleration of the body depends upon two factors,
- the net force acting upon the object and the mass of the object.
The acceleration of an object depends directly
upon the net force acting upon the object,
and inversely upon the mass of the object.
As the force acting upon an object is increased,
the acceleration of the object is increased.
As the mass of an object is increased, the acceleration of the object is decreased.
Source: https://www.physicsclassroom.com/class/newtlaws/Lesson-3/Newton-s-Second-Law
Formulation: Fnet = m • a
Diagrammatic Explanation:
              Forces are unbalanced
                        |
                        |
                        |
                        V
               There is acceleration
                        /\
                       /  \
                      /    \
                     /      \
                    /        \
                   /          \
                  /            \
        __________________   ____ ________________
        |The acceleration |  |The acceleration   |
        |depends directly |  |depends inversely  |
        |on the net Force |  |upon the object's  |
        |_________________|  |mass_______________|
Units:
1 Newton = 1 kg X meters / (seconds^2)
How to use?
Inputs:
    ___________________________________________________
   |Name         | Units                   | Type      |
   |-------------|-------------------------|-----------|
   |mass         | (in kgs)                | float     |
   |-------------|-------------------------|-----------|
   |acceleration | (in meters/(seconds^2)) | float     |
   |_____________|_________________________|___________|

Output:
    ___________________________________________________
   |Name         | Units                   | Type      |
   |-------------|-------------------------|-----------|
   |force        | (in Newtons)            | float     |
   |_____________|_________________________|___________|

"""


def newtons_second_law_of_motion(mass: float, acceleration: float) -> float:
    """
    >>> newtons_second_law_of_motion(10, 10)
    100
    >>> newtons_second_law_of_motion(2.0, 1)
    2.0
    """
    force = float()
    try:
        force = mass * acceleration
    except Exception:
        return -0.0
    return force


if __name__ == "__main__":
    import doctest

    # run doctest
    doctest.testmod()

    # demo
    mass = 12.5
    acceleration = 10
    force = newtons_second_law_of_motion(mass, acceleration)
    print("The force is ", force, "N")
