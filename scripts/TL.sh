#!/bin/bash

echo ""
echo "========================================="
echo "Checking for TexLive manager updates....."
echo "========================================="
echo ""

sudo tlmgr update --self

echo ""
echo "========================================="
echo "Checking for installed package updates..."
echo "========================================="
echo ""


sudo tlmgr update --all
