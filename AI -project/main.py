import tkinter
import tkinter as tk
from collections import defaultdict
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import heapq

class Graph:
  def __init__(self):
    self.graph = defaultdict(list)
    self.actualValues = {} #Uniform Cost and ASTAR
    self.huristic = {} #BEST FIRST SEARCh
    self.huristicPlusCost={} #ASTAR
    self.path=[]
    self.found = False
    self.parentList={}
    self.graphList = []
    self.forwardVisited = []
    self.backwardVisited = []
    self.forwardParentList = {}
    self.backwardParentList = {}
    self.edgeCostList = []

  def addDirectedEdge(self,node,edge):
      self.graph[node].append(edge)
  def addEdge(self,node,edge):

    self.graph[node].append(edge)
    self.graph[edge].append(node)
  def addGraphList(self,node):
      self.graphList.append(node)
  def addHuristic(self,node,hursitic):
      self.huristic[node]=hursitic
  def addCost(self,node1,node2,cost):
    concat = (node1,node2)
    self.actualValues[concat] = cost
    concat = (node2, node1)
    self.actualValues[concat] = cost
    tupple = (node1,node2,cost)
    self.edgeCostList.append(tupple)
  def addDirectCost(self,node1,node2,cost):
      concat = (node1, node2)
      self.actualValues[concat] = cost
  def printGraph(self):
     print(self.graph)
     print(self.actualValues)
     print(self.graphList)
     print(self.huristic)

  # ---------------------------------------------------------------------------Implementing Breadth First Search----------------------------------------------------------------------------------------------
  def BFS(self,start,goal):
   if len(self.path) != 0:
       self.path.clear()
   Que = []
   visited = []
   Que.append(start)
   Found = False
   visited.append(start)
   while Que:
      element = Que.pop(0)
      print(element)
      self.path.append(element)
      if element == goal:
        self.found = True
        break
      for i in self.graph[element]:
       if i not in visited:
        visited.append(i)
        Que.append(i)
   print(self.path)

  # ---------------------------------------------------------------------------Implementing Depth First Search----------------------------------------------------------------------------------------------
  def DFS(self,start,goal):
    if len(self.path) != 0:
          self.path.clear()
    Stack = []
    visited = []
    Stack.append(start)
    Found = False
    visited.append(start)
    while Stack:
       element = Stack.pop()
       print(element)
       self.path.append(element)
       if element == goal:
           self.found = True
           break
       for i in self.graph[element]:
           if i not in visited:
               visited.append(i)
               Stack.append(i)
    print(self.path)

  # ---------------------------------------------------------------------------Implementing Depth Limited Search-------------------------------------------------------------------------------------
  def DLS(self, start,goal,depthLimit=None):
      if len(self.path) != 0:
          self.path.clear()
      if depthLimit is None:
          depthLimit = 3
      depthLimit = depthLimit
      Stack = []
      visited = []
      Stack.append(start)
      self.dict = {}
      visited.append(start)
      while Stack:
          element = Stack.pop()
          depth=0
          tempElement = element
          while tempElement != start:
              if tempElement in self.dict:
                  tempElement = self.dict[tempElement]
                  depth = depth + 1
          if depth > depthLimit:
              continue
          print(element)
          self.path.append(element)
          if element == goal:
              self.found = True
              break
          for i in self.graph[element]:
              if i not in visited:
                  visited.append(i)
                  Stack.append(i)
                  self.dict[i] = element
      print(self.path)
  # ---------------------------------------------------------------------------Implementing Iterative Deepning Search-------------------------------------------------------------------------------------
  def DLSIDS(self, start,goal,depthLimit=None):
      if len(self.path) != 0:
          self.path.clear()
      depthLimit = depthLimit
      Stack = []
      visited = []
      Stack.append(start)
      self.dict = {}
      visited.append(start)
      while Stack:
          element = Stack.pop()
          depth=0
          tempElement = element
          while tempElement != start:
              if tempElement in self.dict:
                  tempElement = self.dict[tempElement]
                  depth = depth + 1
          if depth > depthLimit:
              continue
          print(element)
          self.path.append(element)
          if element == goal:
              self.found = True
              break
          for i in self.graph[element]:
              if i not in visited:
                  visited.append(i)
                  Stack.append(i)
                  self.dict[i] = element
      print(self.path)
  def IterativeDepeeningSearch(self, start, goal):
      if len(self.path) != 0:
          self.path.clear()
      check = False
      i = 1
      while check == False:
          check = self.DLSIDS(start, goal, i)
          i = i + 1
          if check == True:
              break

  # ---------------------------------------------------------------------------Implementing Uniform Cost Search-------------------------------------------------------------------------------------------
  def UCS(self, start, goal):
      if len(self.path) != 0:
          self.path.clear()
      que = []
      heapq.heappush(que, (0, start))
      visited = []
      while que:
          cost, node = heapq.heappop(que)
          if node == goal:
              self.found = True
              tempelement = node
              while tempelement!=start:
                  self.path.append(tempelement)
                  tempelement = self.parentList[tempelement]
              self.path.append(tempelement)
              break
          visited.append(node)
          for neighbour in self.graph[node]:
              if neighbour not in visited:
                  concat = (node, neighbour)
                  newCost = cost + self.actualValues[concat]
                  heapq.heappush(que, (newCost, neighbour))
                  self.parentList[neighbour] = node
      print(self.path)
      print(self.parentList)

  #---------------------------------------------------------------------------Implementing Best First Search----------------------------------------------------------------------------------------------
  def findHeuristic(self, pqueu):
      min = 10000
      node = ""
      for i in pqueu:
          for key, value in self.huristic.items():
              if i == key:
                  if value < min:
                      min = value
                      node = i
      return node

  def BestFirstSearch(self, s, goal):
      if len(self.path) != 0:
          self.path.clear()
      Que = []
      Que.append(s)
      while Que:
          elementToPop = self.findHeuristic(Que)
          for i in range(len(Que)):
              if elementToPop == Que[i]:
                  Que.pop(i)
                  break

          if elementToPop == goal:
              self.found= True
              print(elementToPop)
              self.path.append(elementToPop)
              break;

          print(elementToPop)
          self.path.append(elementToPop)
          for i in self.graph[elementToPop]:
                  Que.append(i)

  # ---------------------------------------------------------------------------Implementing A* Search----------------------------------------------------------------------------------------------
  def findHeuristicAndCost(self, pqueu):
      min = 10000
      node = ""
      for i in pqueu:
          for key, value in self.huristicPlusCost.items():
              if i == key:
                  if value < min:
                      min = value
                      node = i
      return node
  def ASTAR(self, s, goal):
      if len(self.path) != 0:
          self.path.clear()
      Que = []
      Que.append(s)
      visited =[]
      visited.append(s)
      self.huristicPlusCost[s] = 0
      cost = 0
      while Que:
          elementToPop = self.findHeuristicAndCost(Que)
          for i in range(len(Que)):
              if elementToPop == Que[i]:
                  Que.pop(i)
                  break
          if elementToPop == goal:
              self.found = True
              self.path.append(elementToPop)
              break
          self.path.append(elementToPop)
          for i in self.graph[elementToPop]:
                  Que.append(i)
                  visited.append(i)
                  self.parentList[i] = elementToPop
                  tempelement = i
                  while tempelement!=s:
                      parent = self.parentList[tempelement]
                      concat = (parent,tempelement)
                      cost += self.actualValues[concat]
                      tempelement = parent
                  huristic = self.huristic[i]
                  totalCost = cost+huristic
                  self.huristicPlusCost[i] = totalCost
                  totalCost = 0
                  huristic = 0
                  cost=0
                  print(self.huristicPlusCost[i])



     # ---------------------------------------------------------------------------Implementing Bi-directional Search----------------------------------------------------------------------------------------------
  def biDirectionalSearch(self, start, goal):
         if len(self.path) != 0:
          self.path.clear()
         forwardQue = []
         backwardQue = []
         heapq.heappush(forwardQue, (0, start))
         heapq.heappush(backwardQue, (0, goal))
         self.forwardVisited.append(start)
         self.backwardVisited.append(goal)

         while forwardQue and backwardQue:
             forwardCost, forwardNode = heapq.heappop(forwardQue)
             backwardCost, backwardNode = heapq.heappop(backwardQue)
             self.path.append(forwardNode)
             self.path.append(backwardNode)

             if forwardNode in self.backwardVisited:
                 self.found = True
                 self.path.remove(forwardNode)
                 self.path.remove(backwardNode)
                 self.path.extend(self.reversePath(forwardNode))
                 break
             elif backwardNode in self.forwardVisited:
                 self.found = True
                 self.path.remove(forwardNode)
                 self.path.remove(backwardNode)
                 self.path.extend(self.reversePath(backwardNode))
                 break

             self.forwardVisited.append(forwardNode)
             self.backwardVisited.append(backwardNode)

             for neighbour in self.graph[forwardNode]:
                 if neighbour not in self.forwardVisited:
                     concat = (forwardNode, neighbour)
                     newCost = forwardCost + 1
                     heapq.heappush(forwardQue, (newCost, neighbour))
                     self.forwardParentList[neighbour] = forwardNode

             for neighbour in self.graph[backwardNode]:
                 if neighbour not in self.backwardVisited:
                     concat = (backwardNode, neighbour)
                     newCost = backwardCost + 1
                     heapq.heappush(backwardQue, (newCost, neighbour))
                     self.backwardParentList[neighbour] = backwardNode

         print(self.path)

  def reversePath(self, node):
         path = []
         while node:
             path.append(node)
             node = self.forwardParentList.get(node)
         path.reverse()
         return path

  def printGraphList(self):
      G = nx.Graph()
      G.add_edges_from(self.graphList)
      if self.found == True:
          path = self.path
      else:
          path = []
      root = tk.Tk()
      root.title("Graph Visualization")
      weights = self.actualValues
      nx.set_edge_attributes(G, values=weights, name='weight')
      fig = plt.figure(figsize=(5, 5))
      canvas = FigureCanvasTkAgg(fig, master=root)
      canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
      pos = nx.spring_layout(G)
      nx.draw(G, pos, with_labels=True)
      path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
      edge_labels = dict([((u, v), d['weight']) for u, v, d in G.edges(data=True)])
      nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
      nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

      for node in G.nodes():
          x, y = pos[node]
          plt.text(x, y - 0.09, s=str(self.huristic[node]), ha="center", fontsize=14)
      canvas.draw()
      root.mainloop()

  def printDirectedGraphList(self):
      G = nx.DiGraph()
      G.add_edges_from(self.graphList)
      if self.found == True:
          path = self.path
      else:
          path = []
      root = tk.Tk()
      root.title("Graph Visualization")
      weights = self.actualValues
      nx.set_edge_attributes(G, values=weights, name='weight')
      fig = plt.figure(figsize=(5, 5))
      canvas = FigureCanvasTkAgg(fig, master=root)
      canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
      pos = nx.spring_layout(G)
      nx.draw(G, pos, with_labels=True)
      path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
      edge_labels = dict([((u, v), d['weight']) for u, v, d in G.edges(data=True)])
      nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
      nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
      for node in G.nodes():
          x, y = pos[node]
          plt.text(x, y - 0.08, s=str(self.huristic[node]), ha="center", fontsize=14)
      canvas.draw()
      root.mainloop()

def DisplayUI():
 graph = Graph()
 def funcNodes():
        node1 = Node1.get()
        node2 = Node2.get()
        tuple = (node1, node2)
        edge = int(Node3.get())
        if ComboBox1.get() == 'Undirected':
         graph.addEdge(node1,node2)
         graph.addCost(node1,node2,edge)

         graph.addGraphList(tuple)
         graph.printGraph()
         ComboBox1.configure(state="disabled")
         ComboBox1.configure(style="Locked.TCombobox")
        else:
             graph.addDirectedEdge(node1,node2)
             graph.addDirectCost(node1,node2,edge)
             graph.addGraphList(tuple)
             graph.printGraph()
             ComboBox1.configure(state="disabled")
             ComboBox1.configure(style="Locked.TCombobox")



 def getStartNodes():

        startNode = StartNodeEntry.get()
        goalNode = GoalNodeEntry.get()
        if ComboBox.get() == 'BFS':
            graph.BFS(startNode,goalNode)
        elif ComboBox.get() == 'DFS':
            graph.BFS(startNode, goalNode)
        elif ComboBox.get() == 'Unifrom Cost Search':
            graph.UCS(startNode,goalNode)
        elif ComboBox.get() == 'Depth Limited':
            graph.DLS(startNode, goalNode)
        elif ComboBox.get() == 'Iterative Deepning':
            graph.IterativeDepeeningSearch(startNode, goalNode)
        elif ComboBox.get() == 'Bidrectional':
            graph.biDirectionalSearch(startNode, goalNode)
        elif ComboBox.get() == 'Best First':
            graph.BestFirstSearch(startNode, goalNode)
        else:
            graph.ASTAR(startNode, goalNode)

        if ComboBox1.get() == 'Undirected':
         graph.printGraphList()
        else:
            graph.printDirectedGraphList()

 def addHuristicToGraph():
     node = Node.get()
     nodeH = int(NodeH.get())
     graph.addHuristic(node, nodeH)
     graph.printGraph()

 master = tk.Tk()
 Frame = tkinter.Frame(master)
 Frame.pack()
 aiSearches = tkinter.LabelFrame(Frame,text="AI Seaches")
 aiSearches.grid(row=0,column=0)

 labelNode1 = tk.Label(aiSearches, text="Node 1")
 labelNode1.grid(row=0,column=0)
 Node1 = tk.Entry(aiSearches)
 Node1.grid(row=1,column=0,padx=100)

 labelNode2 = tk.Label(aiSearches, text="Node 2")
 labelNode2.grid(row=2,column=0,pady=10)
 Node2 = tk.Entry(aiSearches)
 Node2.grid(row=3,column=0,padx=100,pady=0)

 labelNode3 = tk.Label(aiSearches, text="Edge")
 labelNode3.grid(row=4,column=0,pady=10)
 Node3 = tk.Entry(aiSearches)
 Node3.grid(row=5,column=0,padx=100,pady=0)

 button = tk.Button(aiSearches, text="Add Nodes", command=funcNodes)
 button.grid(row=6,column=0,pady=20)



 labelNode = tk.Label(aiSearches, text="Node")
 labelNode.grid(row=0,column=3)
 Node = tk.Entry(aiSearches)
 Node.grid(row=1,column=3,padx=100)

 labelNodeH = tk.Label(aiSearches, text="Node Huristic")
 labelNodeH.grid(row=2,column=3)
 NodeH = tk.Entry(aiSearches)
 NodeH.grid(row=3,column=3,padx=100,pady=10)

 button3 = tk.Button(aiSearches, text="Add Node Huristic", command=addHuristicToGraph)
 button3.grid(row=4, column=3)



 StartNode = tk.Label(aiSearches, text="Start Node")
 StartNode.grid(row=0,column=4)
 StartNodeEntry = tk.Entry(aiSearches)
 StartNodeEntry.grid(row=1,column=4,padx=100)

 GoalNode = tk.Label(aiSearches, text="Goal Node")
 GoalNode.grid(row=2,column=4)
 GoalNodeEntry = tk.Entry(aiSearches)
 GoalNodeEntry.grid(row=3,column=4,padx=100,pady=10)

 button3 = tk.Button(aiSearches, text="Submit", command=getStartNodes)
 button3.grid(row=4, column=4)

 ChooseAlgo = tk.Label(aiSearches, text="Choose Algorithm")
 ChooseAlgo.grid(row=0, column=5)
 Decision = tk.Label(aiSearches, text="Directed or Undirected")
 Decision.grid(row=2, column=5,pady=10)
 ComboBox = ttk.Combobox(aiSearches,values = ["BFS","DFS","Unifrom Cost Search","Depth Limited","Iterative Deepning","Bidrectional","Best First","A* Search"])
 ComboBox.grid(row=1,column=5)
 ComboBox1 = ttk.Combobox(aiSearches, values=["Directed", "Undirected"])
 ComboBox1.grid(row=3, column=5)
 master.mainloop()

DisplayUI()