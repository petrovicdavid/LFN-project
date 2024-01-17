# Andrea Ghiotto 2118418, David Petrovic 2092073
# Learning From Network project
# Implementation of the computation of the clustering coefficients

import scipy.special

def get_dataset(filename):
    filename = filename.replace("../eigenTriangle/", "")
    filename = filename.replace("../T-Sample/", "")
    filename = filename.replace(".txt", "")
    return filename

if __name__ == "__main__":
    filepath = "../eigenTriangle/result_first.txt"
    #filepath = "../T-Sample/result_first.txt"
    separator = " "
    
    with open(filepath, 'r') as file:
        results = [tuple(map(int, line.strip().split(separator)[:2])) for line in file]

    clustering_coefficients = []

    for tupla in results:
        edges, triangles = tupla
        
        cc = triangles / (6*scipy.special.binom(edges, 3))
        clustering_coefficients.append((cc, edges))

        print("Clustering coefficient: " + str(cc))

    # Save the result (number of edges and approximate number of triangles) in the file.
    result_file = get_dataset(filepath) + "_eigen.txt"
    with open(result_file, "a") as file:
        for tupla in clustering_coefficients:
            file.write(str(tupla[0]) + " " + str(tupla[1]) + "\n")

    print("Result saved!")