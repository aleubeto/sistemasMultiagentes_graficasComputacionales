# Computer Graphics

### 1st Partial Final Homework

Define a ship (*tie-Fighter / imperial destroyer / X-wing*) based on 2D points (array of points x, y)
draw it on the screen in an area of ​​1000 * 600 pixels

Implement functionality:

- (directional arrows) **Translation with respect to the ship orientation**
- (ED) Rotation
- (RF) Scaling

Both the rotation and the scaling should be **with respect ot the ship center**.

Transformations must be persistent (if I scale the object and it gets bigger, if I move it afterwards, it must be moved keeping its large size)

The transformations **has to be done** with homogeneous coordinates.