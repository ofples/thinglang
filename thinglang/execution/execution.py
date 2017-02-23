import traceback
from collections import namedtuple

from thinglang.execution.vm import ITOutput
from thinglang.parser.tokens import MethodCall
import collections

SEGMENT_END = object()
ExecutionOutput = namedtuple('ExecutionOutput', ['output'])

class ExecutionEngine(object):
    def __init__(self, root):
        self.root = root
        self.stack = []
        self.heap = {
            x.value: x for x in root.children
        }

        self.heap['Output'] = ITOutput()

    def results(self):
        return ExecutionOutput(output=self.heap['Output'].data.strip())

    def __enter__(self):
        print('ExecutionEngine: starting')
        print('Parsed tree: {}'.format(self.root.tree()))
        self.print_header()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.print_header()
        print('ExecutionEngine: ended')
        if exc_val:
            print(''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
        print('Program output:')
        self.print_header()
        print(self.heap['Output'].data.strip())
        self.print_header()

    def execute(self):
        self.create_stack_segment(ThingInstance(self.root.find('Program')))

        start = self.root.find('Program').find('start')
        targets = start.children[:]  # clone the list of children
        while targets:
            target = targets.pop(0)

            if target is SEGMENT_END:
                self.stack.pop()
                continue

            if isinstance(target, MethodCall):
                context = self.resolve(self.stack[-1], target.target.value)
                if isinstance(context, collections.Callable):
                    context(target.arguments.evaluate(self.stack[-1]))
                else:
                    self.create_stack_segment(ThingInstance(context.parent))
                    targets = context.children + [SEGMENT_END] + targets
            else:
                target.execute(self.stack[-1])

            if target.children:
                targets = target.children + targets



    def print_header(self):
        print('#' * 80)

    def create_stack_segment(self, instance):
        self.stack.append(StackSegment(instance))

    def resolve(self, stack, target):
        if target[0] == 'self':
            context = stack.instance
            target = target[1:]
        else:
            context = self.heap
        for component in target:
            if component not in context:
                raise ValueError('Cannot find {} in {}'.format(component, context))
            context = context[component]
        return context


class ThingInstance(object):

    def __init__(self, cls):
        self.cls = cls
        self.methods = {
            x.value: x for x in self.cls.children
        }
        self.members = {}

    def __contains__(self, item):
        print(self.methods)
        return item in self.members or item in self.methods

    def __getitem__(self, item):
        return self.members.get(item) or self.methods.get(item)

class StackSegment(object):

    def __init__(self, instance):
        self.instance = instance
        self.data = {}
        self.idx = 0

    def __setitem__(self, key, value):
        print('SET<{}> {}: {}'.format(self.idx, key, value))
        self.data[key] = (self.idx, value)

    def __getitem__(self, item):
        print('GET<{}> {}: {}'.format(self.idx, item, self.data[item][1]))
        return self.data[item][1]

    def __contains__(self, item):
        return item in self.data

    def enter(self):
        print('INCR<{}> -> <{}>'.format(self.idx, self.idx + 1))
        self.idx += 1

    def exit(self):
        print('DECR<{}> -> <{}>'.format(self.idx, self.idx - 1))
        self.data = {
            key: value for key, value in self.data.items() if value[1] != self.idx
        }

        self.idx -= 1


