# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kfp.dsl as dsl


class Coder:
    def __init__(self, ):
        self._code_id = 0

    def get_code(self, ):
        self._code_id += 1
        return '{0:032d}'.format(self._code_id)


dsl.ParallelFor._get_code = Coder().get_code


@dsl.pipeline(name='my-pipeline')
def pipeline(my_pipe_param=10):
    loop_args = [{'a': 1, 'b': 2}, {'a': 10, 'b': 20}]
    with dsl.ParallelFor(loop_args) as item:
        op1 = dsl.ContainerOp(
            name="my-in-coop1",
            image="library/bash:4.4.23",
            command=["sh", "-c"],
            arguments=["echo op1 %s %s" % (item.a, my_pipe_param)],
        )

        op2 = dsl.ContainerOp(
            name="my-in-coop2",
            image="library/bash:4.4.23",
            command=["sh", "-c"],
            arguments=["echo op2 %s" % item.b],
        )

    op_out = dsl.ContainerOp(
        name="my-out-cop",
        image="library/bash:4.4.23",
        command=["sh", "-c"],
        arguments=["echo %s" % my_pipe_param],
    )


if __name__ == '__main__':
    from kfp import compiler
    print(compiler.Compiler().compile(pipeline, package_path=None))
