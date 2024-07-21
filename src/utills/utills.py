from graphviz import Digraph, nohtml
import sys
import json

class PertChart:
    def getInput(self, filename):
        task_list = []
        try:
            '''# this works for input file having one tuple of task per line (cf. v0.3)
            with open(filename) as f:
                for line in f:
                    values = ast.literal_eval(line)
                    task_list.append(values)
            '''
            with open(filename) as f:
                task_list = json.load(f)
        except:
            print("Cannot generate PERT chart. File content of <" + filename + "> cannot be loaded.")
            sys.exit(1)
               
        return task_list
        
    ''' # This is for ES, EF, LS, LF, SL
    def calculateValues(self, p):
        p1 = p
        for k, v in p1.items():
            print(k, v)
            pred = p1[k]["pred"].split(',')
            
            if p1[k]['pred'] == "": #no predecessor
                p1[k]['EF'] = p1[k]['ES'] + p1[k]['D']
                
            elif len(pred) == 1: # 1 predecessor
                key = p1[k]["pred"]

                p1[k]['ES'] = p1[key]['EF'] #EF of predecessor
                p1[k]['EF'] = p1[k]['ES'] + p1[k]['D']
            
            elif len(pred) >1: # 1 predecessor
                print(pred)
                key = pred[1].strip()
                print(key)
                print(p1[key]['EF'])
                p1[k]['ES'] = max(p1[pred[1].strip()]['EF'], p1[pred[1].strip()]['EF']) # list compression
                p1[k]['EF'] = p1[k]['ES'] + p1[k]['D']
                #l = p1[pred[1]]['EF'] # for j in range(len(pred))
                #p1[k]['ES'] = max([p1[pred[j]['EF'] for j in range(len(pred)
        return p1
        '''
    def calculate_values(self, p):
        p1 = {k: v.dict() for k, v in p.items()}  # Convert Pert_Task objects to dictionaries
        for k, v in p1.items():
            pred = p1[k]["pred"]
            if p1[k]['pred'][0] == "START":  # no predecessor
                p1[k]['end'] = p1[k]['start'] + p1[k]['duration']
            elif len(pred) == 1:  # 1 predecessor
                key = p1[k]["pred"][0]
                p1[k]['start'] = p1[key]['end']  # EF of predecessor
                p1[k]['end'] = p1[k]['start'] + p1[k]['duration']
            elif len(pred) > 1:  # more than 1 predecessor
                ends = [p1[p.strip()]['end'] for p in pred]  # list comprehension
                p1[k]['start'] = max(ends)
                p1[k]['end'] = p1[k]['start'] + p1[k]['duration']
        return p1
        
    def create_pert_chart(self, task_list, fill_color = 'grey93', line_color = 'blue'):
        """Gets task list, optional fill_color and line_color and generates PERT chart
            
        Parameters
        ----------
        filename : str
            The file containing task list

        Returns
        -------
        PERT chart diagram
        """
        '''
        task_list = []
        try:
            with open(filename) as f:
                for line in f:
                    values = ast.literal_eval(line)
                    task_list.append(values)
        except:
            print("Cannot generate PERT chart. File does not exist -> " + filename)
            sys.exit(1)
                
        a = task_list
        '''
        a = task_list
        # Graph Instance
        g = Digraph('g', 
                    filename='PERT.gv',
                    node_attr={'shape': 'Mrecord', 
                               'height': '.1'})

        # configurations
        fl_color = fill_color
        ln_color = line_color

        g.attr(rankdir='LR')
        g.attr('node', shape='record')

        # Nodes
        
        '''# this works for input file having one tuple of task per line (cf. v0.3)
        for i in range(len(a)):
            if a[i][0] == "END":
                    continue
            g.node(a[i][0], 
                   nohtml('<f0>' + 
                          a[i][0] + 
                          ' |{' + a[i][1] + '|' + a[i][2] + '|' + a[i][3] + '}|<f2>' + 
                          a[i][4]), 
                   fillcolor=fill_color, 
                   style='filled',
                   color= line_color
                  )
        '''
            
        for k, v in a.items():
            if a[k]['Tid'] == "END":
                continue
            g.node(a[k]["Tid"],
                nohtml('<f0>' +
                    a[k]["Tid"] +
                    ' |{' + str(a[k]["start"]) + '|' + str(a[k]["duration"]) + '|' + str(a[k]["end"]) + '}|<f2>' + a[k]["responsible"]),
                    fillcolor=fl_color,
                    style='filled',
                    color=ln_color
                )

        # Edges
        '''
        g.edge('node0:f2', 'node4:f1') # connect edges with connetion points <f2> and <f1>
        g.edge('node0', 'node1')
        '''

        try:
            ''' # this works for input file having one tuple of task per line (cf. v0.3)
            for i in a: # for rows in a
                #g.edge(i[3] + ':f2', i[0] + ':f0')
                if i[0] == "END":
                    g.edge(i[5], "FINISH")
                else:
                    g.edge(i[5], i[0])
            '''
            for k, v in a.items(): # for task in json task list
                #g.edge(i[3] + ':f2', i[0] + ':f0')
                if a[k]["Tid"] == "END":
                    predecessors = a[k]["pred"]
                    if len(predecessors)>1:
                        for task in predecessors:
                            g.edge(task, a[k]["Tid"])
                    else:
                        g.edge(a[k]["pred"][0], "FINISH")
                else:
                    predecessors = a[k]["pred"]
                    if len(predecessors)>1:
                        for task in predecessors:
                            g.edge(task, a[k]["Tid"])
                    else:
                        g.edge(a[k]["pred"][0], a[k]["Tid"])
        except Exception as e: 
            print("Unexpected error. Check your inputs")
            print(e)
        
        g.render(filename="Pert_image", format='png', cleanup=True)
        

      

