#Maya Python Script

##DAG Hirarchy
Directed Acyclic Graphs is a directed graph that contains no cycles.

In Maya, The DAG is composed of 2 types of DAG nodes
- transforms
    Maintain transformation and parenting information.
    Transform node can have multiple child nodes. 
- shapes
    Reference geometry. Do not provide parenting or transformation infomation
Any piece of geometry requires two DAG nodes above it, a shape node immediately above it, and a transform node above the shape node.

> DAG describes how an instance of an object is **constructed** from a piece of geometry

- **MFnDagNode** - has methods for determining the number of parents and thr parents of a node
- **MFnTransform** - is the function set for operating on transform node (derived from *MFnDagNode*) and has methods to get and set transformation.
- **MFnMesh** - is one of many types of function sets which operate on the many types of shape nodes. (derived from *MFnDagNode*, but not derived from *MFnTransform*)


##Instancing
Whenever a transform or shape node has multiple parent nodes, the node is considered to be instanced. Instancing can be useful to reduce the amount of geometry for a model.

![alt text](http://help.autodesk.com/cloudhelp/2016/ENU/Maya-SDK/images/comp_Transform01.png)

The two valid DAG paths in this graph :
- Transform1 - Transform3 - Leaf
- Transform2 - Transform3 - Leaf

##DAG paths
A path through the DAG is a set of nodes which uniquely identifies the location of the particular node or instance of a node in the graph. The path represents a graph ancestry beginning with the root node of the graph and containing, in succession, a particular child of the root node followed by particular child of this child,etc., down to the node identified by the path. For instanced nodes, there are multiple paths which lead from the root node to the instanced node, one path for each instance.

###why add the shape node to a DAG path
In Maya, selection at the object lebel results in the selection od the transform node that is the parent of the shpae actually selected. When querying the selection using *MGlobal::getActiveSelectionList()*, the *MDagPath* returned to the caller only specifies the path to this transform and not down to the actual shape that was picked on the screen. A convenience method on *MDagPath* called *extendToShape()* can be called to add the shape node below the last transform to the path.

The valid function sets applicable to a particular *MDagPath* are determined by the last node on the path. If the last node is a transform node, then the function sets that can operate on transform nodes can be applied to the *MDagPath* instance. If a shape node is the last node of the path, then the applicable function sets for the *MDagPath* instance are those sets which can operate on the shape.
    
##Examples

![alt text](images/md/dag_outliner.png)
```python
import maya.api.OpenMaya as om

def getDag(name):
    selectionList = om.MSelectionList()
    try:
        selectionList.add(name)
    except:
        return None
        
    dagPath = selectionList.getDagPath(0)
    return dagPath
    
name = #DAG name
dag = om.MFnDagNode(getDag(name))
print name + ' has %s parents' %name, dag.parentCount()
print '[PATH] %s' % dag.getPath()
```
```
pCube1 has 1 parents
[PATH] pCube1

pCube1Shape has 2 parents
[PATH] pCube1|pCube1Shape
-> how to get 2 paths?

pCube1_instance has 1 parents
[PATH] pCube1_instance

group1 has 1 parents
[PATH] group1

pCube1_duplicated has 2 parents
[PATH] group1|pCube1_duplicated

pCube1_duplicatedShape has 1 parents
[PATH] group1|pCube1_duplicated|pCube1_duplicatedShape

group1_instance has 1 parents
[PATH] group1_instance
```

    
