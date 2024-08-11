from board import *
import copy


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class Aier(Player):

    def all_moves(self):

        m1 = []
        m2 = [Rotation.Clockwise]
        m3 = [Rotation.Clockwise, Rotation.Clockwise]
        m4 = [Rotation.Anticlockwise]
        move_rotate = (m1,m2,m3,m4)
        smove = []
        all_move = []
        for cube in move_rotate :
            for k in (Direction.Down,Direction.Left,Direction.Right):
                if k == Direction.Down:
                    all_move.append(cube[:])
                    continue
                for j in range (5):
                    for i in range (j+1):
                        smove.append(k)
                    cube_1 = copy.deepcopy(cube)
                    cube.extend(smove)
                    smove = []
                    all_move.append(cube[:])
                    cube = cube_1
        for cube in all_move:
            cube.extend([Direction.Drop])
        return all_move

    def cacul_of_score(self, line_eliminated_score, landing_height, well_sum, under_block_num):
        a = 0.00023
        b = -1.25
        c = -10
        d = -30
        return float(a*line_eliminated_score**4 + b*landing_height**1.9 + c*well_sum + d*under_block_num)

    def landing_h(self, sandbox, board):
        if len(sandbox.cells) > len(board.cells):
            land = list(set(sandbox.cells).difference(set(board.cells)))
            b = []
            for i in range(len(land)):
                b.append(land[i][1])
            landing_height = 24 - min(b)
        else:
            landing_height = 0
        return landing_height


    def well_sums(self,board):
        well = []
        for y in range(board.height):
            for x in range(board.width):
                if (x, y) not in board.cells:
                    a = x-1 if x>0 else x+1
                    b = x+1 if x<9 else x-1
                    if (a,y) in board.cells and (b,y) in board.cells:
                        well.append((x,y))

        well_set = set(well)
        sum = 0
        for (x,y) in well_set:
            b = y
            while (x,y) in well_set and y < 24:
                y+=1
            sum += (y-b)
        return sum


    def under(self,board):
        under_block = []
        for y in range(board.height):
            for x in range(board.width):
                if (x, y) not in board.cells:
                    for i in range(y):
                        if (x,i) in board.cells:
                            under_block.append((x,y))
                            break
        return (len(under_block))

    def max_h(self, board):
        height = []
        for (x, y) in board.cells:
            height.append(y)
        height.append(24)
        return 24 - min(height)


    def highest_score(self,board):
        all_move = self.all_moves()

        old_score = board.score

        evaluate_score_list = []
        for j in range(len(all_move)):
            sandbox = board.clone()
            for i in range(len(all_move[j])):
                if not sandbox.falling:
                    break
                if all_move[j][i] in [Direction.Drop, Direction.Down, Direction.Left, Direction.Right]:
                    sandbox.move(all_move[j][i])
                elif all_move[j][i] in [Rotation.Anticlockwise, Rotation.Clockwise]:
                    sandbox.rotate(all_move[j][i])
               
            line_eliminated_score = sandbox.score - old_score
            landing_height = self.landing_h(sandbox, board)
            well_sum = self.well_sums(sandbox)
            under_block = self.under(sandbox)
            evaluate_score = self.cacul_of_score(line_eliminated_score, landing_height, well_sum, under_block)
            evaluate_score_list.append(evaluate_score)
        return max(evaluate_score_list)



    def choose_action(self, board):

        all_move = self.all_moves()

        old_score = board.score
        evaluate_score_list = []
        sandbox_collection = []
        for j in range(len(all_move)):
            sandbox = board.clone()

            for i in range(len(all_move[j])):
                if not sandbox.falling:
                    break
                if all_move[j][i] in [Direction.Drop,Direction.Down,Direction.Left,Direction.Right]:
                    sandbox.move(all_move[j][i])
                elif all_move[j][i] in [Rotation.Anticlockwise,Rotation.Clockwise]:
                    sandbox.rotate(all_move[j][i])

          
            line_eliminated_score = sandbox.score - old_score
            landing_height = self.landing_h(sandbox,board)
            well_sum = self.well_sums(sandbox)
            under_block = self.under(sandbox)
            evaluate_score = self.cacul_of_score(line_eliminated_score, landing_height, well_sum, under_block)
            sandbox_collection.append(sandbox)
            evaluate_score_list.append(evaluate_score)


        copy_list = copy.deepcopy(evaluate_score_list)
        copy_list.sort()
        copy_list2 = copy.deepcopy(copy_list[-15:])
        combine_score_list = []
        for i in range(15):
            a = copy_list.pop()
            combine_score_list.insert(0,self.highest_score(sandbox_collection[evaluate_score_list.index(a)])+a)
        index = evaluate_score_list.index(copy_list2[combine_score_list.index(max(combine_score_list))])

        return all_move[index]


SelectedPlayer = Aier
