#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import display_object_distribution
import display_place_region

display_obj_func = display_object_distribution.DisplayObjectDistribution()
display_place_func = display_place_region.DisplayPlaceRegion()


class DisplayLearningResult():
    def __init__(self):
        pass

    def learning_result_draw(self):
        display_obj_func.object_distribution_draw()
        display_place_func.spatial_distribution_draw()
        pass


if __name__ == '__main__':
    rospy.init_node('display_learning_result', anonymous=False)
    display_result = DisplayLearningResult()
    display_result.learning_result_draw()
    rospy.spin()
