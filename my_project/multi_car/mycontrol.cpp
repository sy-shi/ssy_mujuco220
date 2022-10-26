#ifndef CTRL
#define CTRL
#include <mujoco/mujoco.h>
#endif

int multicarnum = 2;
double traj[4];

void generate_traj(const mjModel * m, mjData * d)
{
    traj[0] = d->time*2;
    traj[1] = -d->time*2;
    traj[2] = -d->time*2;
    traj[3] = d->time*2;
};

void controller(const mjModel * m, mjData * d)
{
    generate_traj(m,d);
    d->ctrl[4] = traj[0];
    d->ctrl[6] = traj[1];
    d->ctrl[8] = traj[2];
    d->ctrl[10] = traj[3];
};