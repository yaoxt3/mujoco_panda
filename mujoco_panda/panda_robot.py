import os
from .mujoco_robot import MujocoRobot

MODEL_PATH = os.environ['MJ_PANDA_PATH']+'/mujoco_panda/models/franka_panda.xml'

class PandaArm(MujocoRobot):

    def __init__(self, model_path=MODEL_PATH, render=True):

        super().__init__(model_path, render=render)

        self._has_gripper = self.has_body(['panda_hand','panda_leftfinger','panda_rightfinger'])

        self._logger.info("PandaArm: Robot instance initialised with{} gripper".format("out" if not self._has_gripper else ""))

        if self._has_gripper:
            self.set_as_ee("ee_site")
        else:
            self.set_as_ee("ee_site")

        self._group_actuator_joints()

    @property
    def has_gripper(self):
        return self._has_gripper
    
    def _group_actuator_joints(self):
        arm_joint_names = ["panda_joint{}".format(i) for i in range(1,8)]

        self.actuated_arm_joints = []
        self.actuated_arm_joint_names = []

        self.unactuated_arm_joints = []
        self.unactuated_arm_joint_names = []

        for jnt in arm_joint_names:
            jnt_id = self._model.joint_name2id(jnt)
            if jnt_id in self._movable_joints:
                self.actuated_arm_joints.append(jnt_id)
                self.actuated_arm_joint_names.append(jnt)
            else:
                self.unactuated_arm_joints.append(jnt_id)
                self.unactuated_arm_joint_names.append(jnt)
        
        self._logger.debug("Movable arm joints: {}".format(str(self.actuated_arm_joint_names)))

        self.actuated_gripper_joints = []
        self.actuated_gripper_joint_names = []

        self.unactuated_gripper_joints = []
        self.unactuated_gripper_joint_names = []

        if self._has_gripper:
            gripper_joint_names = ["panda_finger_joint1", "panda_finger_joint2"]

            for jnt in gripper_joint_names:
                jnt_id = self._model.joint_name2id(jnt)
                if jnt_id in self._movable_joints:
                    self.actuated_gripper_joints.append(jnt_id)
                    self.actuated_gripper_joint_names.append(jnt)
                else:
                    self.unactuated_gripper_joints.append(jnt_id)
                    self.unactuated_gripper_joint_names.append(jnt)
            
            self._logger.debug("Movable gripper joints: {}".format(str(self.actuated_gripper_joint_names)))

    def jacobian(self, body_id=None):
        """
        Return body jacobian of end-effector based on the arm joints

        :param body_id: index of end-effector to be used, defaults to "panda_hand" or "panda_link7"
        :type body_id: int, optional
        :return: 6x7 body jacobian
        :rtype: np.ndarray
        """
        return self.body_jacobian(body_id=body_id, joint_indices=self.actuated_arm_joints)

        
