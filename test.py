#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pexpect
import re
from itertools import groupby
from operator import itemgetter

ip="61.147.42.81"
username="zte"
passwd="zteqsc"

result=""

child=pexpect.spawn("telnet %s" % ip)
index=child.expect(["[uU]sername:",pexpect.EOF,pexpect.TIMEOUT])
if index==0:
    child.sendline(username)
    index=child.expect(["[pP]assword:",pexpect.EOF,pexpect.TIMEOUT])
    child.sendline(passwd)
    index=child.expect([".*#",pexpect.EOF,pexpect.TIMEOUT])
    if index==0:
        child.sendline("show vlan-smart-qinq")
        child.expect("show vlan-smart-qinq")
        while True:
            index=child.expect(["--More--","#",pexpect.EOF,pexpect.TIMEOUT])
            if index==0:
                result += child.before
                child.sendline(" ")
            elif index==1:
                result += child.before
                child.close(force=True)
                break
            else:
                child.close(force=True)
                break
    else:
        child.close(force=True)
else:
    child.close(force=True)


temp=result.split('\r\n')
lrst=[x.strip(' \x08') for x in temp if x.strip(' \x08').startswith('epon')]
lrst=[re.split('\s+',x) for x in lrst]
for key, items in groupby(lrst,itemgetter(5)):
    items=list(items)
    if len(items)>1:
        print key
        for i in items:
            print i
        print "-"*20
