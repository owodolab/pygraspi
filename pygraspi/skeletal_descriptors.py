import numpy as np
import doctest

class SkeletalDescriptors:

    def __init__(self, input_data, x_dim, y_dim):
        self.input_data = input_data
        self.x_dim = x_dim
        self.y_dim = y_dim

    def make_morph(self, input_data, x_dim, y_dim):
        return np.reshape(input_data, (y_dim, x_dim))

    def mooreNeighborhood(self, pixel):
        return [[pixel[0]-1, pixel[1]], [pixel[0]-1, pixel[1]+1], [pixel[0], pixel[1]+1],\
                [pixel[0]+1, pixel[1]+1], [pixel[0]+1, pixel[1]], [pixel[0]+1, pixel[1]-1],\
                [pixel[0], pixel[1]-1], [pixel[0]-1, pixel[1]-1]]

    def vonneumanNeighborhood(self, pixel):
        return [[pixel[0]-1, pixel[1]], [pixel[0], pixel[1]-1], [pixel[0], pixel[1]+1], [pixel[0]+1, pixel[1]]]


    def zerotooneTransition(self, moore_neighbors):
        n = moore_neighbors + moore_neighbors[0:1]
        return True if (sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))) == 1 else False

    def getNeighbors(self, morph, n):
        p = []
        for i in n:
            p.append(morph[i[0], i[1]])
        return p

    def firstCondition(self, morph, pixel):

        moore = self.mooreNeighborhood(pixel)
        neighbors = self.getNeighbors(morph, moore)
        if (2 <= sum(neighbors) <= 6) and \
            self.zerotooneTransition(neighbors) == 1 and \
            neighbors[0] * neighbors[2] * neighbors[4] == 0 and \
            neighbors[2] * neighbors[4] * neighbors[6] == 0 :
                return True
        else : return False

    def secondCondition(self, morph, pixel):

        moore = self.mooreNeighborhood(pixel)
        neighbors = self.getNeighbors(morph, moore)
        if (2 <= sum(neighbors) <= 6) and \
            self.zerotooneTransition(neighbors) == 1 and \
            neighbors[0] * neighbors[2] *neighbors[6] == 0 and \
            neighbors[0] * neighbors[4] * neighbors[6] == 0 :
                return True
        else : return False

    def skeletonize2D(self, morph):
        """

        The microstructure is of shape (nx, ny).

        >>> data2 = [0,1,1,1,0,\
                    0,1,1,1,0,\
                    0,1,1,1,0,\
                    0,1,1,1,0]
        >>> nx, ny = 5, 4
        >>> morphology = SkeletalDescriptors(data2, nx, ny)
        >>> morphology2D = morphology.make_morph(data2, nx, ny)
        >>> assert np.allclose(morphology.skeletonize2D(morphology2D), [[0, 1, 1, 1, 0],[0, 0, 1, 0, 0],[0, 0, 1, 0, 0],[0, 1, 1, 1, 0]])

        >>> data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
                    0, 1, 1, 1, 1, 1, 1, 1, 1, 0,\
                    0, 1, 1, 1, 1, 1, 1, 1, 1, 0,\
                    0, 0, 0, 0, 1, 1, 0, 0, 0, 0,\
                    0, 0, 0, 0, 1, 1, 0, 0, 0, 0,\
                    0, 0, 0, 0, 1, 1, 0, 0, 0, 0,\
                    0, 0, 0, 0, 1, 1, 0, 0, 0, 0,\
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        >>> nx, ny = 10, 8
        >>> morphology = SkeletalDescriptors(data, nx, ny)
        >>> morphology2D = morphology.make_morph(data, nx, ny)
        >>> assert np.allclose(morphology.skeletonize2D(morphology2D), [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

        """
        first_condition = second_condition = True
        while first_condition or second_condition:
            first_condition = second_condition = False
            remove_pixel = []
            for i in range(1, morph.shape[0]-1):
                for j in range(1, morph.shape[1]-1):
                    #this_pixel = np.array([i,j])
                    if morph[i, j] == 1 and self.firstCondition(morph,[i, j]):
                        remove_pixel.append([i, j])
                        first_condition = True
            if first_condition:
                for idx in remove_pixel:
                    morph[idx[0], idx[1]] = 0
            remove_pixel = []

            for i in range(1, morph.shape[0]-1):
                for j in range(1, morph.shape[1]):
                    #this_pixel = [i,j]
                    if morph[i, j] == 1 and self.secondCondition(morph, [i, j]):
                        remove_pixel.append([i, j])
                        second_condition = True

            if second_condition:
                for idx in remove_pixel:
                    morph[idx[0], idx[1]] = 0


            return morph


doctest.testmod()
