#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Wentao Han (wentao.han@gmail.com)

# This script waters the love tree on renren.com. It depends on mechanize package.
# Please replace <USERNAME> and <PASSWORD> below with yours.

import logging
import mechanize

# Set logging configuration
logging.basicConfig(format='%(asctime)s %(levelname).1s %(message)s',
                    level=logging.INFO)

# Create the browser and disable processing robots.txt
br = mechanize.Browser()
br.set_handle_robots(False)

# Visit the portal page
br.open('http://m.renren.com/')
logging.info('opened the portal page')

# Log in
br.select_form(nr=0)
br['email'] = '<USERNAME>'
br['password'] = '<PASSWORD>'
br.submit()
logging.info('logged in')

# Go to Love Tree page
br.follow_link(text='个人主页')
br.follow_link(text='情侣空间')
br.follow_link(text='情侣树')
logging.info('went to Love Tree page')

# Shine and water
br.follow_link(text='洒阳光')
br.follow_link(text='洒阳光')
br.follow_link(text='浇水')
br.follow_link(text='浇水')
logging.info('shined and watered')

# Log out
br.follow_link(text='退出')
logging.info('logged out')
