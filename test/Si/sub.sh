#!/bin/bash

export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2

# dptb run task.json -i mix.latest.pth -stu POSCAR -o out
tboptc run task.json -i mix.latest.pth -stu POSCAR -o out
