#!/bin/bash

echo "Select arrangement:"
echo "1 - Sphere swap"
echo "2 - Capsule swap"
echo "3 - Cylinder swap"

read choice

if [ "$choice" = "1" ]; then
    echo "Running Arrangement 1"

    gz service -s /world/interview_world/set_pose \
    --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 2000 \
    --req 'name: "target_box" position: {x: 3.0, y: -0.7, z: 0.15}'

    gz service -s /world/interview_world/set_pose \
    --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 2000 \
    --req 'name: "decoy_sphere" position: {x: 3.0, y: 1.5, z: 0.2}'
fi

if [ "$choice" = "2" ]; then
    echo "Running Arrangement 2"

    gz service -s /world/interview_world/set_pose \
    --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 2000 \
    --req 'name: "target_box" position: {x: 3.0, y: 0.0, z: 0.15}'

    gz service -s /world/interview_world/set_pose \
    --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 2000 \
    --req 'name: "decoy_capsule" position: {x: 3.0, y: 1.5, z: 0.25}'
fi

if [ "$choice" = "3" ]; then
    echo "Running Arrangement 3"

    gz service -s /world/interview_world/set_pose \
    --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 2000 \
    --req 'name: "target_box" position: {x: 3.0, y: 0.7, z: 0.15}'

    gz service -s /world/interview_world/set_pose \
    --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 2000 \
    --req 'name: "decoy_cylinder" position: {x: 3.0, y: 1.5, z: 0.15}'
fi
