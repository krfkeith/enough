import pygame
import random

from App import App
from Widget import Widget
from Lib import Graph

from Lib.Point import Point

from guilib import get_default

class NodeValue(object):
    def __init__(self, name, start_pos=None):
        self.name = name
        self.start_pos = get_default(start_pos, Point(0,0))

    def set_widget(self, widget):
        self._widget = widget
        self.update_widget_text()
        self._widget.pos.final = self.start_pos
    def get_widget(self):
        return self._widget
    widget = property(fget=get_widget,fset=set_widget)
    
    def update_widget_text(self):
        self._widget.text = self.name

class GraphWidget(Widget):
    def __init__(self, *args, **kw):
        super(GraphWidget, self).__init__(*args, **kw)
        self.out_connection_lines = []
        
    def set_node(self, node):
        self.node = node
        node.value.widget = self

    def connect_pos(self, upper=False):
        y = self.size.current.y * 0.5
        return self.pos.current + Point(self.size.current.x * 0.5, y)

    def iter_visible_nodes(self, nlist):
        for out_node in nlist:
            w = out_node.value.widget
            if not w.params.visible:
                continue
            yield w
    def iter_visible_connected(self, dir):
        for w in self.iter_visible_nodes(self.node.connections[dir]):
            yield w
            
    def paint_connections(self, surface):
        if self.node is None:
            return
        
        #for w in self.iter_visible_connected('in'):
        #    pygame.draw.aalines(surface, (200,20,50), False, (self.connect_pos().as_tuple(), w.connect_pos().as_tuple()), True)
        for line in self.out_connection_lines:
            pygame.draw.aalines(surface, (200,20,50), False, line, True)
            #for p in line:
            #    pygame.draw.circle(surface, (200,50,50), p, 2, 0)

        
class GraphApp(App):
    def __init__(self, *args, **kw):
        super(GraphApp, self).__init__(*args, **kw)
        from Lib.Dot import Dot
        self.dot = Dot()
        
    def add_nodes(self, nodes):
        for node in nodes:
            w = GraphWidget()
            w.set_node(node)
            self.add_widget(w)
        self.update_layout()            

    def zoom(self, zoom):
        for widget in self.widgets:
            widget.font_size.final = widget.font_size.final * zoom
        self._paint(None)

    def paint_widgets(self, event):
        #self.update_layout()
        for w in self.widgets:
            w.paint_connections(self.screen)
        super(GraphApp, self).paint_widgets(event)
        
    def _key_up(self, e):
        super(GraphApp, self)._key_up(e)
        if (e.mod & pygame.KMOD_CTRL):
            if e.key == pygame.K_w:
                self.zoom(1.3)
            elif e.key == pygame.K_q:
                self.zoom(1/(1.3))

    def update_layout(self):
        nodes = [widget.node for widget in self.widgets]
        g, n, e = Graph.get_drawing_data(self.dot, nodes)
        x_scale = self.width / float(g['width'])
        y_scale = self.height / float(g['height'])
        for node, n_layout in n.iteritems():
            node.value.widget.pos.final.x = n_layout['x'] * x_scale/1.2
            node.value.widget.pos.final.y = n_layout['y'] * y_scale/1.2
            node.value.widget.size.final.x = n_layout['width'] * x_scale/1.2
            node.value.widget.size.final.y = n_layout['height'] * y_scale/1.2
            node.value.widget.pos.final = node.value.widget.pos.final - node.value.widget.size.final * 0.5

        for node, n_layout in n.iteritems():
            lines = []
            if node not in e:
                continue
            for edge in e[node]:
                this = node.value.widget
                other = edge['tail_node'].value.widget
                
                line = [Point(int(p[0]*x_scale/1.2), int(p[1]*y_scale/1.2)) for p in edge['points']]
                line.reverse() # the direction is always tail->head, so we reverse it

                from Lib.Bezier import Bezier
                curves = [p.as_tuple() for p in Bezier(line, 10)]
                
                
                curves.insert(0, (this.pos.final+this.size.final*0.5).as_tuple())
                curves.append((other.pos.final+other.size.final*0.5).as_tuple())
                
                lines.append(curves)
            node.value.widget.out_connection_lines = lines
            
            #print node.value.widget.pos.final
            #node.value.widget.size.final.x = n_layout['width']
            #node.value.widget.size.final.y = n_layout['height']
        
            

#---------------------------------------------


def test():
    a = GraphApp()

    import random
    random.seed(0)
    nodes = []
    for i in xrange(15):
        pos = Point(10*random.random() - 5, 10*random.random() - 5)
        pos = pos + Point(a.width, a.height)*0.5
        n1 = Graph.Node(NodeValue(str(i), pos))
        if nodes:
            n1.connect_out(random.choice(nodes))
            if (random.random() > 0.1):
                n1.connect_in(random.choice(nodes))
        nodes.append(n1)

    a.add_nodes(nodes)
    
    a.run()

if __name__=='__main__':
    test()