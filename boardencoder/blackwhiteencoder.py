# #### BEGIN LICENSE BLOCK #####
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
#
# Contributor(s):
#
#    Bin.Li (ornot2008@yahoo.com)
#
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# #### END LICENSE BLOCK #####
#
# /
import numpy as np

from common.encoder import Encoder
from common.point import Point


class BlackWhiteEncoder(Encoder):
    def __init__(self, num_plane, board_size):
        self._board_size = board_size
        self._board_width = board_size
        self._board_height = board_size
        self._num_plane = num_plane

    def name(self):
        return 'BlackWhiteEncoder'

    @property
    def num_plane(self):
        return self._num_plane

    @property
    def board_width(self):
        return self._board_width

    @property
    def board_height(self):
        return self._board_height

    def encode(self, boards, player_in_action, previous_move=None):
        board_matrix = np.zeros(self.shape(), dtype=int)

        # The previous number of planes
        for plane in range(len(boards)):
            for row in range(self._board_height):
                for col in range(self._board_width):
                    point = Point(row+1, col+1)
                    piece = boards[plane].get_piece_at_point(point)
                    if piece.owner_id != -1:
                        if piece.owner_id == player_in_action:
                            board_matrix[plane*2+1, row, col] = 1
                        else:
                            board_matrix[plane*2, row, col] = 1

        #  the  last move
        for row in range(self._board_height):
            for col in range(self._board_width):
                flag = 0
                if previous_move is not None and row == previous_move.point.row-1 and col == previous_move.point.col-1:
                    flag = 1

                board_matrix[self._num_plane*2, row, col] = flag

        #  the  player who will play in the next move
        for row in range(self._board_height):
            for col in range(self._board_width):
                board_matrix[self._num_plane*2+1,
                             row, col] = player_in_action

        return board_matrix

    def shape(self):
        return self._num_plane*2+2, self._board_height, self._board_width

    def encode_point(self, point):
        return self._board_width*(point.row-1)+(point.col-1)

    def decode_point_index(self, index):
        row = index // self._board_width
        col = index % self._board_width
        return Point(row=row+1, col=col+1)

    def num_points(self):
        return self._board_width*self._board_height
