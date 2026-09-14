import numpy as np
from stl import mesh

def create_revoltech_ankle_joint():
    """
    Generate a 3D model of an 8mm Revoltech ball joint ankle connector.
    """
    
    # Dimensions (in mm)
    ball_diameter = 8.0
    ball_radius = ball_diameter / 2
    shaft_diameter = 3.8
    shaft_radius = shaft_diameter / 2
    total_height = 16.0
    socket_diameter = 8.2
    socket_radius = socket_diameter / 2
    
    resolution = 32
    
    vertices = []
    faces = []
    
    def add_sphere(center, radius, start_vertex_idx):
        sphere_vertices = []
        sphere_faces = []
        
        for i in range(resolution):
            lat = np.pi * i / resolution
            for j in range(resolution):
                lon = 2 * np.pi * j / resolution
                
                x = center[0] + radius * np.sin(lat) * np.cos(lon)
                y = center[1] + radius * np.sin(lat) * np.sin(lon)
                z = center[2] + radius * np.cos(lat)
                
                sphere_vertices.append([x, y, z])
        
        for i in range(resolution - 1):
            for j in range(resolution):
                v1 = start_vertex_idx + i * resolution + j
                v2 = start_vertex_idx + i * resolution + (j + 1) % resolution
                v3 = start_vertex_idx + (i + 1) * resolution + j
                v4 = start_vertex_idx + (i + 1) * resolution + (j + 1) % resolution
                
                sphere_faces.append([v1, v2, v3])
                sphere_faces.append([v2, v4, v3])
        
        return sphere_vertices, sphere_faces
    
    def add_cylinder(center, radius, height, start_vertex_idx):
        cyl_vertices = []
        cyl_faces = []
        
        for j in range(resolution):
            angle = 2 * np.pi * j / resolution
            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)
            
            cyl_vertices.append([x, y, center[2] + height / 2])
            cyl_vertices.append([x, y, center[2] - height / 2])
        
        for j in range(resolution):
            j_next = (j + 1) % resolution
            
            v1 = start_vertex_idx + j * 2
            v2 = start_vertex_idx + j * 2 + 1
            v3 = start_vertex_idx + j_next * 2
            v4 = start_vertex_idx + j_next * 2 + 1
            
            cyl_faces.append([v1, v3, v2])
            cyl_faces.append([v3, v4, v2])
        
        top_center_idx = start_vertex_idx + resolution * 2
        cyl_vertices.append([center[0], center[1], center[2] + height / 2])
        for j in range(resolution):
            j_next = (j + 1) % resolution
            v1 = start_vertex_idx + j * 2
            v2 = start_vertex_idx + j_next * 2
            cyl_faces.append([v1, top_center_idx, v2])
        
        bottom_center_idx = start_vertex_idx + resolution * 2 + 1
        cyl_vertices.append([center[0], center[1], center[2] - height / 2])
        for j in range(resolution):
            j_next = (j + 1) % resolution
            v1 = start_vertex_idx + j * 2 + 1
            v2 = start_vertex_idx + j_next * 2 + 1
            cyl_faces.append([v1, v2, bottom_center_idx])
        
        return cyl_vertices, cyl_faces
    
    vertex_count = 0
    
    # Top ball joint
    top_ball_center = [0, 0, total_height / 2]
    sphere_verts, sphere_faces = add_sphere(top_ball_center, ball_radius, vertex_count)
    vertices.extend(sphere_verts)
    for face in sphere_faces:
        faces.append(face)
    vertex_count += len(sphere_verts)
    
    # Main cylindrical shaft
    shaft_height = total_height - ball_diameter
    cyl_verts, cyl_faces = add_cylinder([0, 0, 0], shaft_radius, shaft_height, vertex_count)
    vertices.extend(cyl_verts)
    for face in cyl_faces:
        faces.append(face)
    vertex_count += len(cyl_verts)
    
    # Bottom socket
    socket_center = [0, 0, -(total_height / 2 - 4.0)]
    socket_verts, socket_faces = add_sphere(socket_center, socket_radius, vertex_count)
    vertices.extend(socket_verts)
    for face in socket_faces:
        faces.append(face)
    
    vertices = np.array(vertices)
    faces = np.array(faces)
    
    revoltech_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            revoltech_mesh.vectors[i][j] = vertices[face[j]]
    
    return revoltech_mesh

if __name__ == "__main__":
    ankle_mesh = create_revoltech_ankle_joint()
    ankle_mesh.save("revoltech_ankle_joint_8mm.stl")
    print("STL file generated: revoltech_ankle_joint_8mm.stl")
