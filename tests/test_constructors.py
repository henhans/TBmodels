#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    04.07.2016 14:01:18 CEST
# File:    test_invalid_constructors.py

import itertools

import pytest
import tbmodels

from models import get_model

def test_on_site_too_long(get_model):
    with pytest.raises(ValueError):
        get_model(0.1, 0.2, on_site=[1, 2, 3])

def test_no_size_given(get_model, models_equal):
    model1 = get_model(0.1, 0.2, size=None)
    model2 = get_model(0.1, 0.2)
    models_equal(model1, model2)
    
def test_size_unknown(get_model):
    with pytest.raises(ValueError):
        get_model(0.1, 0.2, size=None, on_site=None)

def test_add_on_site(get_model, models_equal):
    model1 = get_model(0.1, 0.2, on_site=(1, -2))
    model2 = get_model(0.1, 0.2, size=2, on_site=None)
    model2.add_on_site((1, -2))
    models_equal(model1, model2)
    
def test_invalid_add_on_site(get_model):
    model = get_model(0.1, 0.2)
    with pytest.raises(ValueError):
        model.add_on_site((1, 2, 3))

def test_explicit_dim(get_model, models_equal):
    model1 = get_model(0.1, 0.2, dim=3)
    model2 = get_model(0.1, 0.2)
    models_equal(model1, model2)

def test_no_dim(get_model, models_equal):
    with pytest.raises(ValueError):
        get_model(0.1, 0.2, pos=None)

def test_pos_outside_uc(get_model, models_equal):
    model1 = get_model(0.1, 0.2, pos=((0., 0., 0.), (-0.5, -0.5, 0.)))
    model2 = get_model(0.1, 0.2)
    models_equal(model1, model2)

def test_from_hopping_list(get_model, models_equal):
    t1 = 0.1
    t2 = 0.2
    hoppings = []
    for phase, R in zip([1, -1j, 1j, -1], itertools.product([0, -1], [0, -1], [0])):
        hoppings.append([t1 * phase, 0, 1, R])

    for R in ((*r, 0) for r in itertools.permutations([0, 1])):
        hoppings.append([t2, 0, 0, R])
        hoppings.append([-t2, 1, 1, R])
    model1 = tbmodels.Model.from_hopping_list(size=2, hopping_list=hoppings)
    model2 = get_model(t1, t2)
    models_equal(model1, model2)
