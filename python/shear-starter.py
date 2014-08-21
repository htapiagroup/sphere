#!/usr/bin/env python
import sphere
import numpy
import sys

# launch with:
# $ python shear-starter <DEVICE> <C_PHI> <C_GRAD_P> <SIGMA_0>

device = int(sys.argv[1])
c_phi = float(sys.argv[2])
c_grad_p = float(sys.argv[3])
sigma0 = float(sys.argv[4])

sim = sphere.sim('diffusivity-sigma0=' + str(sigma0) + '-c_phi=' + \
        str(c_phi) + '-c_grad_p=' + str(c_grad_p), fluid=True)
sim.readlast()

sim.sid = 'shear-sigma0=' + str(sigma0) + '-c_phi=' + str(c_phi) + \
        '-c_grad_p=' + str(c_grad_p)
print(sim.sid)


sim.checkerboardColors(nx=6,ny=6,nz=6)
sim.cleanup()
sim.adjustUpperWall()
sim.zeroKinematics()

sim.shear()

sim.initFluid(mu = 17.87e-4, p = 1.0e5, hydrostatic = True)
sim.setFluidBottomNoFlow()
sim.setFluidTopFixedPressure()
sim.setDEMstepsPerCFDstep(10)
sim.setMaxIterations(2e5)
sim.initTemporal(total = 20.0, file_dt = 0.01, epsilon=0.07)
sim.c_phi[0] = c_phi
sim.c_grad_p[0] = c_grad_p

# Fix lowermost particles
dz = sim.L[2]/sim.num[2]
I = numpy.nonzero(sim.x[:,2] < 1.5*dz)
sim.fixvel[I] = 1

sim.run(dry=True)
sim.run(device=device)
#sim.writeVTKall()
sim.visualize('walls')
sim.visualize('fluid-pressure')