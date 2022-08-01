#!/usr/bin/env python

#Imports de mensagens ( Checar se são as mesmas no ROS2 com o ros2 echo)
from geometry_msgs.msg  import Twist # MENSAGEM COMANDO VELOCIDADE
from turtlesim.msg import Pose # MENSAGEM POSIÇÃO

# Import de função base do python
from math import pow,atan2,sqrt

# Imports para nó do ros
import rclpy
from rclpy.node import Node

TOPIC_CMD = "/turtle1/cmd_vel" # TOPICO COMANDO VELOCIDADE
TOPIC_POSE = "/turtle1/pose" # TOPICO COMANDO POSIÇÃO TARTARUGA

KP_LINEAR = 1.5
KP_ANGULAR = 4

# Classe utilizada para calcular nosso turble bot 
class turtlebot(Node):
    def __init__(self):
        super().__init__('turtle_gotogoal')
        # Declaração de quem vai publicar, tipo de variável TWIST e tópico
        self.publisher = self.create_publisher(Twist, TOPIC_CMD, 10)
        # Declaração de quem vai escutar, tipo de variável POSE, tópico e função de callback
        self.subscription = self.create_subscription(Pose, TOPIC_POSE,self.callback,10)
        # Previne o erro de variavel nao utilizada 
        self.subscription
        # Variaveis utilizadas para armazenar nossa posição
        self.pose = Pose()

    
    #Callback function implementing the pose value received
    def callback(self, msg):
        self.pose = msg 
        self.get_logger().info('Pose MSG: "%s"' % msg)
        
     
    # Função para calcular distancia
    def get_distance(self, goal):
        distance = sqrt(pow((goal.x - self.pose.x), 2) + pow((goal.y - self.pose.y), 2))
        #COLOCAR PRINT DISTANCE
        return distance

    def get_angular_distance(self,goal):
        angular_distance = (atan2(goal.y - self.pose.y, goal.x - self.pose.x) - self.pose.theta)
        #COLOCAR PRINT ANGULAR DISTANCE       
        return angular_distance

    # Função que move o robo para um local especifico
    # Recebe o input do usuario e enquanto não chegar no destino não para de enviar
    def move2goal(self):
        # Recebe os inputs do usuario
        goal_pose = Pose()
        goal_pose.x = float(input("Set your x goal:"))
        goal_pose.y = float(input("Set your y goal:"))
        distance_tolerance = float(input("Set your tolerance:"))
        vel_msg = Twist()

        # Aplica um controle de acordo com a formula de posição
        # Checkar variaveis e tipo de mensagem
        while self.get_distance(goal_pose) >= distance_tolerance:
            # Controle ERROR = SETPOINT - FEEDBACK ---> SETPOINT = GOAL_POSE / FEEDBACK = POSE
            #Porportional Controller
            #linear velocity in the x-axis:
            vel_msg.linear.x = KP_LINEAR * self.get_distance(goal_pose)
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0

            #angular velocity in the z-axis:
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = KP_ANGULAR * self.get_angular_distance(goal_pose)

            #Publishing our vel_msg
            self.publisher.publish(vel_msg)
            self.get_logger().info('Velocity published MSG: "%s"' % vel_msg)
        
        #Publishing our vel_msg
        self.get_logger().info('Goal reached')

        #Stopping our robot after the movement is over
        vel_msg.linear.x = 0.0
        vel_msg.angular.z =0.0
        self.publisher.publish(vel_msg)

# Função main utilizada para rodar o codigo
def main(args=None):
    rclpy.init(args=args)

    # Função para inicializar o turtlebot
    go_to_goal = turtlebot()

    # Função para mover to goal
    go_to_goal.move2goal()

    # A funçao spin era utilizada para fazer com que o codigo continuasse roddnado    
    rclpy.spin(go_to_goal)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    go_to_goal.destroy_node()

    rclpy.shutdown()
       
if __name__ == '__main__':
    #Testing our function
    main()
