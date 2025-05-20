
#  BSD LICENSE
#
#  Copyright (c) Crane Chu <cranechu@gmail.com>
# -*- coding: utf-8 -*-


import time
import pytest
import logging

import nvme as d

def test_customizedTest35(nvme0):
    nvme0n1=d.Namespace(nvme0,nsid=10)
    # nvme0n1.inject_write_buffer_disable()
    logging.info("\n".join(dir(nvme0)))
    logging.info("\n".join(dir(nvme0n1)))

def test_customizedTest34(pciaddr):
    b = d.Buffer(4096, "Testing Buffer",1)
    logging.info(b[:16])
    logging.info(b[496:521])
    p=d.Pcie(pciaddr)
    nvme0=d.Controller(p)    

    nvme0n1=d.Namespace(nvme0,nsid=1)
    # nvme0n1.inject_write_buffer_disable()
    qpair = d.Qpair(nvme0, 16)
    nvme0n1.write(qpair, b, 0, 2).waitdone()
    logging.info(b[:15])
    logging.info(b[496:521])


def test_customizedTest33(pciaddr):
    b = d.Buffer(260, "Test on buffer 0, 0", 0, 0)
    logging.info(b.dump())
    b2 = d.Buffer(260, "Test on buffer 1", 1)
    logging.info(b2.dump())
    b3 = d.Buffer(260, "Test on buffer  1, 32", 1, 32)
    logging.info(b3.dump())
    b4 = d.Buffer(260, "Test on buffer 0x12345678, 32", 0x12345678, 32)
    logging.info(b4.dump())
    b5 = d.Buffer(260, "Test on buffer 0, 0xbeef", 0, 0xbeef)
    logging.info(b5.dump())
    b6 = d.Buffer(260, "Test on buffer 1, 0xbeef", 1, 0xbeef)
    logging.info(b6.dump())
    b7 = d.Buffer(260, "Test on buffer 50, 0xbeef", 50, 0xbeef)
    logging.info(b7.dump())
    b8 = d.Buffer(260, "Test on buffer 99, 0xbeef", 99, 0xbeef)
    logging.info(b8.dump())
    b9 = d.Buffer(260, "Test on buffer file pattern.bin", 0xf17e)
    logging.info(b9.dump())
    b = d.Buffer(260, "Test on buffer incr", pvalue=0x1, ptype=0x1234)    ##dunno why is it not functioning
    logging.info(b.dump())
    b11 = d.Buffer(260, "Test on buffer decr", 0x1333, 0x4321)          #dunno why is it not functioning
    logging.info(b11.dump())


def test_customizedTest32(pciaddr):
    p=d.Pcie(pciaddr)
    b=d.Buffer(4096)
    nvme0=d.Controller(p)
    nvme0.identify(b).waitdone()
    nvme0.getfeatures(0x1)



def test_customizedTest30(nvme0n1):
    logging.info(nvme0n1.get_lba_format(512, 0) )
    logging.info(nvme0n1.get_lba_format(512, 8) )
    logging.info(nvme0n1.get_lba_format(512, 16) )
    # logging.info(nvme0n1.get_lba_format(512, 32) )
    logging.info(nvme0n1.get_lba_format(4096, 0) )
    logging.info(nvme0n1.get_lba_format(4096, 8) )
    logging.info(nvme0n1.get_lba_format(4096, 16) )
    # logging.info(nvme0n1.get_lba_format(4096, 32) )
    logging.info(nvme0n1.get_lba_format() )
    assert nvme0n1.get_lba_format(4096, 0) != nvme0n1.get_lba_format(512, 0)
    assert nvme0n1.get_lba_format(4097, 0) == None
    assert nvme0n1.get_lba_format() < 16


# def test_customizedTest29(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     n = d.Controller(pcie)
#     b1 = d.Buffer(1024)

#     ascii_chars = list(range(0x20, 0x7F))  # 0x20 到 0x7E，95 个字符
#     repeat_chars = list(range(0x01, 0x7F))  # 0x01 到 0x7E，126 个字符
#     pattern = ascii_chars + repeat_chars   # 总共 95 + 126 = 221 个字符

#     fill_data = []
#     for i in range(1024):
#         fill_data.append(pattern[i % len(pattern)])

#     b1[0:] = fill_data

#     print(b1.dump())
#     q=d.Qpair(n,16)
#     ns=d.Namespace(n,1)
#     ns.write(q,b1,0,2,io_flags=1).waitdone
#     print(b1.dump()) ##found 0x000 and 0x1f0 have data lost





def test_customizedTest28(pciaddr):
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)
    ns = d.Namespace(nvme0, nsid=1)
    q = d.Qpair(nvme0, 16)
    
    ns.write_uncorrectable(q, lba=0, lba_count=1).waitdone()
    logging.info("Write Uncorrectable done")
    
    ns.write_zeroes(q, lba=0, lba_count=1, io_flags=0).waitdone()
    logging.info("Write Zeroes done")
    
    q.delete()
    ns.close()
    pcie.close()




def test_customizedTest27(pciaddr):
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)
    ns = d.Namespace(nvme0, nsid=1)
    b=d.Buffer(1024)
    q=d.Qpair(nvme0,16)
    ns.get_lba_format()
    logging.info(ns.get_lba_format(16,4))


def test_customizedTest26(pciaddr):
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)
    ns = d.Namespace(nvme0, nsid=1)
    b=d.Buffer(1024)
    q=d.Qpair(nvme0,16)
    ns.flush(q)



def test_customizedTest25(pciaddr):
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)
    ns = d.Namespace(nvme0, nsid=1)
    b=d.Buffer(1024)
    q=d.Qpair(nvme0,16)
    #ns.write_uncorrectable(q, lba=0, lba_count=100000).waitdone()
    worker_result=ns.ioworker(io_size=8,          # 4KB IO size
                                lba_random=True,    # Random LBA access
                                qdepth=16,          # Queue depth
                                read_percentage=50, # 50% read, 50% write
                                time=3,pvalue=0).start().close()
    
    # logging.info(worker_result)

    print(f"{'IO Count Read':<20}: {worker_result.io_count_read:>10}")
    print(f"{'IO Count Nonread':<20}: {worker_result.io_count_nonread:>10}")
    print(f"{'IO Count Write':<20}: {worker_result.io_count_write:>10}")
    print(f"{'Milliseconds':<20}: {worker_result.mseconds:>10}")
    print(f"{'Latency Max (us)':<20}: {worker_result.latency_max_us:>10}")
    print(f"{'Latency Avg (us)':<20}: {worker_result.latency_average_us:>10}")
    print(f"{'CPU Usage':<20}: {worker_result.cpu_usage:>10.4f}")
    print(f"{'Error':<20}: {worker_result.error:>10}")




def test_customizedTest24(pciaddr):
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)
    ns = d.Namespace(nvme0, nsid=1)
    b=d.Buffer(1024)
    q=d.Qpair(nvme0,16)
    logging.info(ns.compare(q,b,0))
    pcie.close()




################################################namespace################################################


def test_customizedTest23(pciaddr):
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)
    nvme0.init_ns()
    ns = d.Namespace(nvme0, nsid=1)
    
    wbuf = d.Buffer(512)  
    rbuf = d.Buffer(512)
    wbuf[0:] = b"DATA 1234567890 ABCDEFGHIJKLMNOP"
    print(f"Written data before: {wbuf.dump(48)}")
    
    qpair = d.Qpair(nvme0, 16)
    nvme0.send_cmd(0x01, wbuf, nsid=1, cdw10=0, cdw11=1).waitdone()  ## 0x01 is io write command
    # ns.write(qpair,wbuf,0,1).waitdone()
    print(f"Written data after: {wbuf.dump(48)}")
    
    #nvme0.send_cmd(0x02, rbuf, nsid=1, cdw10=0, cdw11=1).waitdone()  ## 0x02 is io read command
    ns.read(qpair, rbuf, 0, 1).waitdone()
    print(f"Read data: {rbuf.dump(48)}")
    
    qpair.delete()
    pcie.close()



def test_customizedTest22(pciaddr):
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)
    nvme0.init_ns()
    ns = d.Namespace(nvme0, nsid=1)
    
    wbuf = d.Buffer(512)  # 假设块大小512字节
    rbuf = d.Buffer(512)
    wbuf[0:30] = b"DATA 1234567890 ABCDEFGHIJKLMNOP"
    print(f"Written data before: {wbuf.dump(64)}")
    
    qpair = d.Qpair(nvme0, 16)
    nvme0.send_cmd(0x01, wbuf, nsid=1, cdw10=0, cdw11=1).waitdone() #lower level command # NVMe Write命令   ## also same result with previous   ###solved
    '''                                                             #sometime can sometime still making data disappear
    cdw10=0：告诉设备从哪个块开始操作，这里是第 0 块（起始位置）。
    cdw11=1：告诉设备操作多少块，这里是 1 块（数量）。
    就像告诉快递员：“从第 0 个房子开始，送 1 个包裹。”
    '''
    
    print(f"Written data after: {wbuf.dump(64)}")
    
    ns.read(qpair, rbuf, 0, 1).waitdone()
    print(f"Read data: {rbuf.dump(64)}")
    
    qpair.delete()
    pcie.close()



def test_customizedTest21(pciaddr):
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)
    nvme0.init_ns()
    ns = d.Namespace(nvme0, nsid=1)
    
    wbuf = d.Buffer(1024)
    rbuf = d.Buffer(1024)
    wbuf[0:30] = b"DATA 1234567890 ABCDEFGHIJKLMNOP"
    print(f"Written data before: {wbuf.dump(32)}")
    
    # 复制缓冲区
    write_copy = d.Buffer(1024)
    write_copy[0:30] = wbuf[0:30]
    
    qpair = d.Qpair(nvme0, 16)
    ns.write(qpair, write_copy, 0, 1).waitdone()
    print(f"Written data after: {wbuf.dump(32)}")  # 检查原始缓冲区
    print(f"Copy after write: {write_copy.dump(32)}")  # 检查写入缓冲区
    
    ns.read(qpair, rbuf, 0, 1).waitdone()
    print(f"Read data: {rbuf.dump(32)}")
    
    qpair.delete()
    pcie.close()


# def test_customizedTest20_ivan(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     nvme0 = d.Controller(pcie)
#     nvme0.init_ns()
#     ns = d.Namespace(nvme0, nsid=1)
    
#     wbuf = d.Buffer(1024)  
#     rbuf = d.Buffer(1024)
#     # buf[0:11] = b"DATA ABCDEFG"  
#     wbuf[4:] = b"DATA 1234567890 ABCDEFGHIJKLMNOPQRST"     ## start from the 0th slot
#     #wbuf[8:30] = b"DATA 1234567890 ABCDEFGHIJKLMNOP"      ## start from the 9th slot


#     print(f"Written data: {wbuf.dump(48)}")
#     qpair = d.Qpair(nvme0, 32)
    
#     ns.write(qpair, wbuf, 0, 1).waitdone()  
#     print(f"Written data: {wbuf.dump(48)}")
#     ns.read(qpair, rbuf, 0, 1).waitdone()  

#     print(f"Read data: {rbuf.dump(48)}")
#     qpair.delete()
#     pcie.close()


# def test_customizedTest20(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     nvme0 = d.Controller(pcie)
#     nvme0.init_ns()
#     ns = d.Namespace(nvme0, nsid=1)
    
#     wbuf = d.Buffer(1024)  
#     rbuf = d.Buffer(1024)
#     # buf[0:11] = b"DATA ABCDEFG"  
#     wbuf[0:30] = b"DATA 1234567890 ABCDEFGHIJKLMNOP"     ## start from the 0th slot
#     #wbuf[8:30] = b"DATA 1234567890 ABCDEFGHIJKLMNOP"      ## start from the 9th slot


#     print(f"Written data: {wbuf.dump(48)}")
#     qpair = d.Qpair(nvme0, 32)
    
#     ns.write(qpair, wbuf, 0, 1).waitdone()  
#     print(f"Written data: {wbuf.dump(48)}")
#     ns.read(qpair, rbuf, 0, 1).waitdone()  

#     print(f"Read data: {rbuf.dump(48)}")
#     qpair.delete()
#     pcie.close()
#     '''
#     #### start from 0th slot
# Written data: buffer
# [0x00000000]  44 41 54 41 20 31 32 33  34 35 36 37 38 39 30 20  DATA 1234567890 
# [0x00000010]  41 42 43 44 45 46 47 48  49 4a 4b 4c 4d 4e 4f 50  ABCDEFGHIJKLMNOP

# Written data: buffer
# [0x00000000]  00 00 00 00 00 00 00 00  34 35 36 37 38 39 30 20  ........4567890     ##data is changed
# [0x00000010]  41 42 43 44 45 46 47 48  49 4a 4b 4c 4d 4e 4f 50  ABCDEFGHIJKLMNOP

# Read data: buffer
# [0x00000000]  00 00 00 00 00 00 00 00  34 35 36 37 38 39 30 20  ........4567890 
# [0x00000010]  41 42 43 44 45 46 47 48  49 4a 4b 4c 4d 4e 4f 50  ABCDEFGHIJKLMNOP





# ##########strat from 9th slot

# Written data: buffer
# [0x00000000]  00 00 00 00 00 00 00 00  44 41 54 41 20 31 32 33  ........DATA 123
# [0x00000010]  34 35 36 37 38 39 30 20  41 42 43 44 45 46 47 48  4567890 ABCDEFGH
# [0x00000020]  49 4a 4b 4c 4d 4e 4f 50  00 00 00 00 00 00 00 00  IJKLMNOP........

# Written data: buffer
# [0x00000000]  00 00 00 00 00 00 00 00  44 41 54 41 20 31 32 33  ........DATA 123
# [0x00000010]  34 35 36 37 38 39 30 20  41 42 43 44 45 46 47 48  4567890 ABCDEFGH
# [0x00000020]  49 4a 4b 4c 4d 4e 4f 50  00 00 00 00 00 00 00 00  IJKLMNOP........

# Read data: buffer
# [0x00000000]  00 00 00 00 00 00 00 00  44 41 54 41 20 31 32 33  ........DATA 123
# [0x00000010]  34 35 36 37 38 39 30 20  41 42 43 44 45 46 47 48  4567890 ABCDEFGH
# [0x00000020]  49 4a 4b 4c 4d 4e 4f 50  00 00 00 00 00 00 00 00  IJKLMNOP........


    
    
#     '''


# def test_customizedTest19(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     nvme0 = d.Controller(pcie)
#     nvme0.init_ns()
#     ns = d.Namespace(nvme0, nsid=1)
#     buf = d.Buffer(4096)  # 分配4KB缓冲区
#     rbuf=d.Buffer(4096)
#     buf[0:11] = b"DATA ABCDEFG"  # 写入数据
    
#     # 创建 I/O 队列对
#     qpair = d.Qpair(nvme0, 64)  # 队列深度为16，可以根据需要调整
#     ns.write(qpair, buf, 0, 8).waitdone()  # 使用队列对写入数据到LBA 0，8个块

#     ns.read(qpair, rbuf, 0, 8).waitdone()  # 从LBA 0读取8个块
#     print(f"Read data: {rbuf[0:12]}")
    
#     qpair.delete()  # 清理队列对
#     pcie.close()




# def test_customizedTest18(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     nvme0 = d.Controller(pcie)
#     nvme0.init_ns()
#     ns = d.Namespace(nvme0, nsid=1)
#     buf = d.Buffer(4096)  # 分配4KB缓冲区
#     buf[0:4] = b"DATA"  # 写入数据
#     ns.write(buf,0,8).waitdone()  # 写入到LBA 0，8个块 ##required 3 argument to run and already have 1 argument ??    ## solved, the argument cannot add in variable
#     pcie.close()                                                                                                    ## But new error come out : FAILED driver_test.py::test_customizedTest - TypeError: Cannot convert nvme.Buffer to nvme.Qpair
#                                                                                                                     ## test19 solve this

# def test_customizedTest17(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     nvme0 = d.Controller(pcie)
#     # nvme0.init_ns()
#     ns = d.Namespace(nvme0, nsid=1)  # 初始化命名空间ID为1
#     pcie.close()



# def test_customizedTest16(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     nvme0 = d.Controller(pcie)
#     buf = d.Buffer(512)  # 分配缓冲区
#     nvme0.send_cmd(opcode=0xFF, buf=buf, nsid=1, cdw10=0x12345678).waitdone()  # 发送命令到命名空间ID为1
#     pcie.close()



# def test_customizedTest15(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     nvme0 = d.Controller(pcie)
#     nvme0.init_ns()  # 初始化所有命名空间
#     pcie.close()



# def test_customizedTest14(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     nvme0 = d.Controller(pcie)
#     buf = d.Buffer(4096)  # 分配一个4KB缓冲区
#     nvme0.identify(buf, nsid=1, cns=0).waitdone()  # 获取命名空间ID为1的识别数据
#     print(nvme0.identify(buf,cdw11=1))
#     # print(buf.dump(64))  
#     # pcie.close()

# #########################################################Controller###################################################################3

# def test_customizedTest13(pciaddr):
#     pcie = d.Pcie(pciaddr)     
#     nvme0 = d.Controller(pcie)
#     nvme0.timeout = 5  #ms  
#     print(f"Current timeout: {nvme0.timeout} ms")
#     pcie.close()



# def test_customizedTest12(pciaddr):
#     pcie = d.Pcie(pciaddr)     
#     nvme0 = d.Controller(pcie)
#     ##print(dir(nvme0.supports() ))
#     #is_supported = nvme0.supports(opcode=0x00)  # 检查是否支持Identify命令
#     #print(f"Identify command supported: {is_supported}")


# def test_customizedTest11(pciaddr):
#     pcie = d.Pcie(pciaddr)     
#     nvme0 = d.Controller(pcie)
#     nvme0.setfeatures(fid=0x07, cdw11=(15 << 16) + 15).waitdone()  # 设置队列数特性


# def test_customizedTest10(pciaddr):
#     pcie = d.Pcie(pciaddr)     
#     nvme0 = d.Controller(pcie)
#     buf = d.Buffer(512)  # 分配接收缓冲区
#     buf[0:4] = b"SECU"  # 填充数据
#     print(buf[0:4])
#     nvme0.security_send(buf=buf, spsp=0x5678, secp=1, nssf=0, size=512).waitdone()
#     pcie.close()


# def test_customizedTest9(pciaddr):
#     pcie = d.Pcie(pciaddr)     
#     nvme0 = d.Controller(pcie)
#     buf = d.Buffer(512)  # 分配接收缓冲区
#     nvme0.security_receive(buf=buf, spsp=0x1234, secp=1, nssf=0, size=512).waitdone()
#     print(buf[0:100])  # 打印接收到的安全数据
#     pcie.close()


# def test_customizedTest8(pciaddr):
#     pcie = d.Pcie(pciaddr)     
#     nvme0 = d.Controller(pcie)
#     buf = d.Buffer(4096,"testing buffer")
#     nvme0.sanitize(option=0x1, pattern=0xDEADBEEF).waitdone()  # 执行sanitize操作




# def test_customizedTest7(pciaddr):
#     pcie = d.Pcie(pciaddr)     
#     nvme0 = d.Controller(pcie)
#     buf = d.Buffer(4096,"testing buffer")
#     buf[0:4] = b"TEST on pynvme, halo this is ivan"  # 填充数据
#     nvme0.mi_send(opcode=0x02, dword0=0x1234, dword1=0x5678, buf=buf, mtype=1).waitdone()
#     logging.info(buf.dump(1024))
#     pcie.close()



# def test_customizedTest6(pciaddr):
#     pcie = d.Pcie(pciaddr)     
#     nvme0 = d.Controller(pcie)
#     buf = d.Buffer(4096,"testing buffer")
#     nvme0.identify(buf).waitdone() 
#     print(buf.dump(64)) 



# def test_customizedTest5(pciaddr):
#     pcie = d.Pcie(pciaddr)      #sometime the controller will suddenly cant be created
#     nvme0 = d.Controller(pcie)
#     buf = d.Buffer(512)  # 分配缓冲区
#     nvme0.send_cmd(opcode=0xFF, buf=buf, nsid=1, cdw10=0x12345678).waitdone(expected=1)  # 发送通用命令 ##expected=1 # 等待1个命令完成
#     pcie.close()


# def test_customizedTest4(pciaddr):
#     pcie = d.Pcie(pciaddr)
#     nvme0 = d.Controller(pcie)
#     nvme0.reset()
#     nvme0.init_adminq()# 初始化管理队列
#     nvme0.init_ns()  

#     # latency = nvme0.latest_latency  # 获取最近完成命令的延迟（单位：微秒）#also lag
#     # print(f"Latest command latency: {latency} us")    #nothing came out
#     ##logging.info(nvme0.init_queues(cdw9=0x00010001))  # 初始化队列，设置特定值 # will lag at there
#     # pcie.close()


#     # pcie1 = d.Pcie(pciaddr)
#     # nvme0 = d.Controller(pcie1)
#     # buf = d.Buffer(512)  # 分配发送缓冲区
#     # buf[0:4] = b"SECU"  # 填充数据
#     # nvme0.security_send(buf=buf, spsp=0x5678, secp=1, nssf=0, size=512).waitdone()




# def test_customizedTest3(pciaddr):   #Controller
#     b=d.Buffer()
#     pcie = d.Pcie(pciaddr)
#     n = d.Controller(pcie)
#     ns=d.Namespace(n,10)
#     n.identify(b, nsid=0, cns=1).waitdone()
#     print(b.dump(900))
#     # print(hex(n[0]))
#     # print(hex(n[0x1c]))

#     #print(n.cmdlog(1))
#     #print(n.id_data(23,4,str))

#     # #n.cmdname(00)
#     # print(n.cmdname(0x00))  #Delete I/O Submission Queue 
#     # print(n.cmdname(0xa))   #Get Features
#     # print(n.cmdname(0x7))   #unknown opcode command
#     # print(n.cmdname(0x2a))  #unknown opcode command
    

#     # b=d.Buffer(1024,'testOnController')
#     ## n.identify(b).waitdone()    #identify need some more argument, find it out
#     # print(b.dump(64))

#     ##print(n.downfw("/home/jj/.local/pynvme",0x01))
    
#     # print(dir(n.format(0)))
#     # print(n.format(0))
#     # n.format(0x02)






# def test_customizedTest2(pciaddr):    #namespace
#     pcie = d.Pcie(pciaddr)
#     n = d.Controller(pcie)
#     ns=d.Namespace(n,10)
#     logging.info(dir(ns))
#     #logging.info(ns.capacity())
#     #ns.compare()
#     # with ns.ioworker(time=1):
#     #     pass
#     logging.info(ns.ioworker(time=1))
#     qpair=d.Qpair(n,16)
#     #print(dir(qpair))
#     print(hex(n[0x1c]))
#     b = d.Buffer(2048, 'pynvme_example')
#     print(n.supports(0x80))
#     # print(dir(n.identify()))
#     #n.abort()
#     #print(b.dump(16))
    
#     # logging.info(n)
#     # print(n.supports(0x18))
#     # #print(n.id_data(10,4,str))
#     # print(n.cmdlog(2))
#     # n.init_ns()
    

# ################################################Buffer#################################################3



# def test_customizedTest1(): #Buffer
#     b = d.Buffer(2048, 'pynvme_example')
#     b2 = d.Buffer(1024, 'pynvme_example2')
#     b[0]=0x6a
#     b[1:7]=[1,2]
#     b[7:8]=[0x2,0x31,4,5,6,91,0x67,9,2,0x5a,0x5b,0x5c,0x6,0x7,8,0x5a]
#     print(b.dump(50))
#     print(len(b))
#     print(b[1])



@pytest.mark.parametrize("repeat", range(2))
def test_init_nvme_back_compatibility(pciaddr, repeat):
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)
    logging.info(hex(pcie.register(0, 4)))
    nvme0n1 = d.Namespace(nvme0, 1)
    nvme0n1.format(512)

    with nvme0n1.ioworker(time=1), \
            nvme0n1.ioworker(time=1):
        pass
    nvme0n1.close()
    pcie.close()


# intuitive, spec, qpair, vscode, debug, cmdlog, assert
def test_hello_world(nvme0, nvme0n1, qpair):
    # prepare data buffer and IO queue
    #print(nvme0)
    #print(nvme0n1)

    # logging.info(nvme0n1)
    # print(qpair)
    # logging.info(qpair)
    read_buf = d.Buffer()
    #print(type(qpair))
    #logging.info(read_buf)
    write_buf = d.Buffer()
    #print(write_buf)
    #logging.info(write_buf)
    write_buf[10:21] = b'hello world'

    # send write and read command
    def write_cb(cdw0, status1):  # command callback function
     #  print(cdw0)
     #  print(status1)
        nvme0n1.read(qpair, read_buf, 0, 1)

    nvme0n1.write(qpair, write_buf, 0, 1, cb=write_cb)

    # wait commands complete and verify data
    assert read_buf[10:21] != b'hello world'
    qpair.waitdone(2)
    assert read_buf[10:21] == b'hello world'


# access PCIe/NVMe registers, identify data, pythonic
def test_registers_and_identify_data(pcie, nvme0, nvme0n1):
    # logging.info(pcie[0], pcie.register(0, 2))
    logging.info("0x%x, 0x%x" % (pcie[0], pcie.register(0, 2)))
    logging.info("0x%08x, 0x%08x" % (nvme0[0], nvme0[4]))
    logging.info("model name: %s" % nvme0.id_data(63, 24, str))
    logging.info("vid: 0x%x" % nvme0.id_data(1, 0))
    logging.info("namespace size: %d" % nvme0n1.id_data(7, 0))


# Controller, sanitize, default parameters, getlogpage
def test_sanitize(nvme0: d.Controller, buf):
    if nvme0.id_data(331, 328) == 0:
        pytest.skip("sanitize operation is not supported")

    #import PySimpleGUI as sg

    logging.info("supported sanitize operation: %d" % nvme0.id_data(331, 328))
    #sg.OneLineProgressMeter('sanitize progress', 0, 100, 'progress', orientation='h')
    nvme0n1 = d.Namespace(nvme0, 1, 128*1000*1000//4)
    nvme0.sanitize().waitdone()  # sanitize clears namespace

    # check sanitize status in log page
    nvme0.getlogpage(0x81, buf, 20).waitdone()
    while buf.data(3, 2) & 0x7 != 1:  # sanitize operation is not completed
        time.sleep(1)
        nvme0.getlogpage(0x81, buf, 20).waitdone()
        progress = buf.data(1, 0)*100//0xffff
        #sg.OneLineProgressMeter('sanitize progress', progress, 100, 'progress', orientation='h')
        logging.info("%d%%" % progress)

    nvme0n1.close()


# simple ioworker, complicated io_size, python function call, CI
def test_ioworker_simplified(nvme0, nvme0n1: d.Namespace, qpair):
    nvme0n1.ioworker(time=1).start().close()
    nvme0n1.ioworker(io_size=[1, 2, 3, 7, 8, 16], time=1).start().close()
    nvme0n1.ioworker(op_percentage={2:10, 1:20, 0:30, 9:40}, time=1).start().close()
    test_hello_world(nvme0, nvme0n1, qpair)
    logging.info(test_hello_world(nvme0, nvme0n1, qpair))


# ioworker with admin commands, multiprocessing, log, cmdlog, pythonic
def subprocess_trim(pciaddr, seconds):
    pcie = d.Pcie(pciaddr)
    # print(pciaddr)
    # print(pcie)
    nvme0 = d.Controller(pcie, True)
    #print(nvme0)
    nvme0n1 = d.Namespace(nvme0)
    #print(nvme0n1)
    q = d.Qpair(nvme0, 8)
    #print(q)
    buf = d.Buffer(4096)
    #print(buf)
    buf.set_dsm_range(0, 8, 8)

    # send trim commands
    start = time.time()
    while time.time()-start < seconds:
        nvme0n1.dsm(q, buf, 1).waitdone()

    q.delete()
    nvme0n1.close()
    pcie.close()

def test_ioworker_with_temperature_and_trim(nvme0, nvme0n1):
    test_seconds = 2

    # start trim process
    import multiprocessing
    mp = multiprocessing.get_context("spawn")
    p = mp.Process(target = subprocess_trim,
                   args = (nvme0.addr, test_seconds))
    p.start()

    # start read/write ioworker and admin commands
    smart_log = d.Buffer(512, "smart log")
    with nvme0n1.ioworker(io_size=256,
                          lba_random=False,
                          read_percentage=0,
                          time=test_seconds):
        for i in range(15):
            time.sleep(1)
            nvme0.getlogpage(0x02, smart_log, 512).waitdone()
            ktemp = smart_log.data(2, 1)

            from pytemperature import k2c
            logging.info("temperature: %0.2f degreeC" % k2c(ktemp))

    # wait trim process complete
    p.join()


# multiple ioworkers, PCIe, TCP, CPU, performance, ioworker return values
def test_multiple_controllers_and_namespaces(pciaddr):
    # address list of the devices to test
    addr_list = ['01:00.0', '02:00.0', '03:00.0', '04:00.0']
    addr_list = [pciaddr, ]
    test_seconds = 10

    # create all controllers and namespace
    pcie_list = [d.Pcie(a) for a in addr_list]
    nvme_list = [d.Controller(p) for p in pcie_list]
    ns_list = [d.Namespace(n) for n in nvme_list]

    # create two ioworkers on each namespace
    ioworkers = []
    for ns in ns_list:
        print(ns)
        w = ns.ioworker(io_size=8, lba_align=8,
                        region_start=0, region_end=256*1024*8, # 1GB space
                        lba_random=False, qdepth=64,
                        read_percentage=100, time=test_seconds).start()
        ioworkers.append(w)
        w = ns.ioworker(io_size=8, lba_align=16,
                        region_start=256*1024*8, region_end=2*256*1024*8,
                        lba_random=True, qdepth=256,
                        read_percentage=0, time=test_seconds).start()
        ioworkers.append(w)

    # collect test results
    io_total = 0
    for w in ioworkers:
        logging.info(w)
        r = w.close()
        io_total += (r.io_count_read+r.io_count_nonread)
    logging.info("total throughput: %d IOPS" % (io_total/test_seconds))

    for n in ns_list:
        n.close()

    for p in pcie_list:
        p.close()


# PCIe, different of power states and resets
# def test_power_and_reset(pcie, nvme0, subsystem):
#     print(subsystem)
#     pcie.aspm = 2              # ASPM L1
#     pcie.power_state = 3       # PCI PM D3hot
#     pcie.aspm = 0
#     pcie.power_state = 0

#     nvme0.reset()              # controller reset: CC.EN
#     nvme0.getfeatures(7).waitdone()

#     pcie.reset()               # PCIe reset: hot reset, TS1, TS2
#     nvme0.reset()              # reset controller after pcie reset
#     nvme0.getfeatures(7).waitdone()

#     pcie.flr()                 # PCIe function level reset
#     nvme0.reset()              # reset controller after pcie reset
#     nvme0.getfeatures(7).waitdone()

#     subsystem.reset()          # NVMe subsystem reset: NSSR
#     nvme0.reset()              # controller reset: CC.EN
#     nvme0.getfeatures(7).waitdone()

#     subsystem.power_cycle(10)  # power cycle NVMe device: cold reset
#     nvme0.reset()              # controller reset: CC.EN
#     nvme0.getfeatures(7).waitdone()

#     subsystem.poweroff()
#     subsystem.poweron()
#     nvme0.reset()              # controller reset: CC.EN
#     nvme0.getfeatures(7).waitdone()


# test parameters, leverage innovations in python community
@pytest.mark.parametrize("io_count", [1, 9])
@pytest.mark.parametrize("lba_count", [1, 8])
@pytest.mark.parametrize("lba_offset", [0, 8])
def test_different_io_size_and_count(nvme0, nvme0n1, qpair,
                                     lba_offset, lba_count, io_count):
    # allcoate all DMA buffers for IO commands
    bufs = []
    for i in range(io_count):
        bufs.append(d.Buffer(lba_count*512))

    # send and reap all IO command dwords
    for i in range(io_count):
        nvme0n1.read(qpair, bufs[i], lba_offset, lba_count)
    qpair.waitdone(io_count)


# IO commands, fused operations, generic commands
def test_fused_operations(nvme0, nvme0n1):
    # create qpair and buffer for IO commands
    q = d.Qpair(nvme0, 10)
    b = d.Buffer()

    # separate compare and write commands
    nvme0n1.write(q, b, 8).waitdone()
    nvme0n1.compare(q, b, 8).waitdone()

    # implement fused compare and write operations with generic commands
    # Controller.send_cmd() sends admin commands,
    # and Namespace.send_cmd() here sends IO commands.
    nvme0n1.send_cmd(5|(1<<8), q, b, 1, 8, 0, 0)
    nvme0n1.send_cmd(1|(1<<9), q, b, 1, 8, 0, 0)
    q.waitdone(2)
    q.delete()


# protocol tests on queue, buffer, PRP, and doorbells
from psd import IOCQ, IOSQ, PRP, PRPList, SQE, CQE
def test_send_cmd_2sq_1cq(nvme0):
    # 2 SQ share one CQ
    cq = IOCQ(nvme0, 1, 10, PRP())
    sq1 = IOSQ(nvme0, 1, 10, PRP(), cqid=1)
    sq2 = IOSQ(nvme0, 2, 16, PRP(), cqid=1)
    print(cq,sq1,sq2)

    # write lba0, 16K data organized by PRPList
    write_cmd = SQE(1, 1)       # write to namespace 1
    write_cmd.prp1 = PRP()      # PRP1 is a 4K page
    prp_list = PRPList()        # PRPList contains 3 pages
    prp_list[0] = PRP()
    prp_list[1] = PRP()
    prp_list[2] = PRP()
    write_cmd.prp2 = prp_list   # PRP2 points to the PRPList
    write_cmd[10] = 0           # starting LBA
    write_cmd[12] = 31          # LBA count: 32, 16K, 4 pages
    write_cmd.cid = 123         # verify cid later

    # send write commands in both SQ
    sq1[0] = write_cmd          # fill command dwords in SQ1
    write_cmd.cid = 567         # verify cid later
    sq2[0] = write_cmd          # fill command dwords in SQ2
    sq2.tail = 1                # ring doorbell of SQ2 first
    time.sleep(0.1)             # delay to ring SQ1,
    sq1.tail = 1                #  so command in SQ2 should complete first

    # wait for 2 command completions
    while CQE(cq[1]).p == 0: pass

    # check first cpl
    cqe = CQE(cq[0])
    assert cqe.sqid == 2
    assert cqe.sqhd == 1
    assert cqe.cid == 567

    # check second cpl
    cqe = CQE(cq[1])
    assert cqe.sqid == 1
    assert cqe.sqhd == 1
    assert cqe.cid == 123

    # update cq head doorbell to device
    cq.head = 2

    # delete all queues
    sq1.delete()
    sq2.delete()
    cq.delete()


def test_sanitize_operations_basic(nvme0, nvme0n1):  #L8
    if nvme0.id_data(331, 328) == 0:  #L9
        pytest.skip("sanitize operation is not supported")  #L10

    logging.info("supported sanitize operation: %d" % nvme0.id_data(331, 328))
    nvme0.sanitize().waitdone()  #L13

    # check sanitize status in log page
    buf = d.Buffer(4096)  #L16
    with pytest.warns(UserWarning, match="AER notification is triggered"):
        nvme0.getlogpage(0x81, buf, 20).waitdone()  #L17
        while buf.data(3, 2) & 0x7 != 1:  #L18
            time.sleep(1)
            nvme0.getlogpage(0x81, buf, 20).waitdone()  #L20
            progress = buf.data(1, 0)*100//0xffff
            logging.info("%d%%" % progress)


def test_buffer_read_write(nvme0, nvme0n1):
    buf = d.Buffer(512, 'ascii table')  #L2
    logging.info("physical address of buffer: 0x%lx" % buf.phys_addr)  #L3

    for i in range(512):
        buf[i] = i%256  #L6
    print(buf.dump(128))  #L7

    buf = d.Buffer(512, 'random', pvalue=100, ptype=0xbeef)  #L15
    print(buf.dump())
    buf = d.Buffer(512, 'random', pvalue=100, ptype=0xbeef)  #L17
    print(buf.dump())

    qpair = d.Qpair(nvme0, 10)
    nvme0n1.write(qpair, buf, 0).waitdone()
    nvme0n1.read(qpair, buf, 0).waitdone()
    print(buf.dump())
    qpair.delete()


@pytest.fixture()
def ncqa(nvme0):
    num_of_queue = 0
    def test_greater_id(cdw0, status):
        nonlocal num_of_queue
        num_of_queue = 1+(cdw0&0xffff)
    nvme0.getfeatures(7, cb=test_greater_id).waitdone()
    logging.info("number of queue: %d" % num_of_queue)
    return num_of_queue

def test_create_qpairs(nvme0, nvme0n1, buf, ncqa):
    qpair = d.Qpair(nvme0, 1024)
    nvme0n1.read(qpair, buf, 0)
    qpair.waitdone()
    nvme0n1.read(qpair, buf, 0, 8).waitdone()

    ql = []
    for i in range(ncqa-1):
        ql.append(d.Qpair(nvme0, 8))

    with pytest.raises(d.QpairCreationError):
        ql.append(d.Qpair(nvme0, 8))

    with pytest.warns(UserWarning, match="ioworker host ERROR -1: "):
        nvme0n1.ioworker(io_size=8, time=1000).start().close()

    qpair.delete()
    nvme0n1.ioworker(io_size=8, time=1).start().close()

    for q in ql:
        q.delete()


def test_namespace_multiple(pciaddr, buf):
    # create all controllers and namespace
    addr_list = [pciaddr, ] # add more DUT BDF here
    pcie_list = [d.Pcie(a) for a in addr_list]

    for p in pcie_list:
        nvmex = d.Controller(p)
        qpair = d.Qpair(nvmex, 8)
        nvmexn1 = d.Namespace(nvmex)

        #Check if support write uncorrectable command
        wuecc_support = nvmex.id_data(521, 520) & 0x2
        if wuecc_support != 0:
            nvmexn1.write_uncorrectable(qpair, 0, 8).waitdone()
            with pytest.warns(UserWarning, match="ERROR status: 02/81"):
                nvmexn1.read(qpair, buf, 0, 8).waitdone()

            nvmexn1.write(qpair, buf, 0, 8).waitdone()
            def this_read_cb(dword0, status1):
                assert status1>>1 == 0
                nvmexn1.write_uncorrectable(qpair, 0, 8)
            nvmexn1.read(qpair, buf, 0, 8, cb=this_read_cb).waitdone(2)

            def another_read_cb(dword0, status1):
                logging.info("dword0: 0x%08x" % dword0)
                logging.info("phase bit: %d" % (status1&1))
                logging.info("dnr: %d" % ((status1>>15)&1))
                logging.info("more: %d" % ((status1>>14)&1))
                logging.info("sct: 0x%x" % ((status1>>9)&0x7))
                logging.info("sc: 0x%x" % ((status1>>1)&0xff))
            with pytest.warns(UserWarning, match="ERROR status: 02/81"):
                nvmexn1.read(qpair, buf, 0, 8, cb=another_read_cb).waitdone()

        qpair.delete()
        nvmexn1.close()
        p.close()


@pytest.mark.parametrize("qcount", [1, 1, 2, 4])
def test_ioworker_iops_multiple_queue(nvme0n1, qcount):
    nvme0n1.format(512)

    l = []
    io_total = 0
    for i in range(qcount):
        a = nvme0n1.ioworker(io_size=8, lba_align=8,
                             region_start=0, region_end=256*1024*8, # 1GB space
                             lba_random=False, qdepth=16,
                             read_percentage=100, time=10).start()
        l.append(a)

    for a in l:
        r = a.close()
        io_total += r.io_count_read

    logging.info("Q %d IOPS: %.3fK" % (qcount, io_total/10000))


@pytest.mark.parametrize("iops", [100, 10*1000, 1000*1000])
def test_ioworker_fixed_iops(nvme0n1, iops):
    output_io_per_second = []
    nvme0n1.ioworker(io_size=8,
                     lba_random=True,
                     read_percentage=100,
                     iops=iops,
                     output_io_per_second=output_io_per_second,
                     time=10).start().close()
    logging.info(output_io_per_second)


def test_dsm_trim(nvme0: d.Controller, nvme0n1: d.Namespace, qpair: d.Qpair):
    trimbuf = d.Buffer(4096)

    # DUT info
    logging.info("model number: %s" % nvme0.id_data(63, 24, str))
    logging.info("firmware revision: %s" % nvme0.id_data(71, 64, str))

    # single range
    start_lba = 0
    lba_count = 8*1024
    trimbuf.set_dsm_range(0, start_lba, lba_count)
    nvme0n1.dsm(qpair, trimbuf, 1, attribute=0x4).waitdone()

    # multiple range
    lba_count = lba_count//256
    for i in range(256):
        trimbuf.set_dsm_range(i, start_lba+i*lba_count, lba_count)
    nvme0n1.dsm(qpair, trimbuf, 256).waitdone()


def test_ioworker_performance(nvme0n1):
    import matplotlib.pyplot as plt

    output_io_per_second = []
    percentile_latency = dict.fromkeys([90, 99, 99.9, 99.99, 99.999])
    nvme0n1.ioworker(io_size=8,
                     lba_random=True,
                     read_percentage=100,
                     output_io_per_second=output_io_per_second,
                     output_percentile_latency=percentile_latency,
                     time=10).start().close()
    logging.info(output_io_per_second)
    logging.info(percentile_latency)

    X = []
    Y = []
    for _, k in enumerate(percentile_latency):
        X.append(k)
        Y.append(percentile_latency[k])

    plt.plot(X, Y)
    plt.xscale('log')
    plt.yscale('log')
    #plt.show()


def test_ioworker_jedec_enterprise_workload(nvme0n1):
    distribution = [1000]*5 + [200]*15 + [25]*80
    iosz_distribution = {1: 4,
                         2: 1,
                         3: 1,
                         4: 1,
                         5: 1,
                         6: 1,
                         7: 1,
                         8: 67,
                         16: 10,
                         32: 7,
                         64: 3,
                         128: 3}

    nvme0n1.ioworker(io_size=iosz_distribution,
                     distribution = distribution,
                     lba_random=True,
                     read_percentage=0,
                     ptype=0xbeef, pvalue=100,
                     time=10).start().close()


# def test_power_on_off(nvme0):
#     def poweron():
#         logging.info("poweron")
#         pass
#     def poweroff():
#         logging.info("poweroff")
#         pass
#     subsystem = d.Subsystem(nvme0, poweron, poweroff)

#     subsystem = d.Subsystem(nvme0)
#     subsystem.poweroff()
#     subsystem.poweron()
#     nvme0.reset()


def test_init_nvme_customerized(pcie):
    def nvme_init(nvme0):
        logging.info("user defined nvme init")

        nvme0[0x14] = 0
        while not (nvme0[0x1c]&0x1) == 0: pass

        # 3. set admin queue registers
        nvme0.init_adminq()

        # 4. set register cc
        nvme0[0x14] = 0x00460000

        # 5. enable cc.en
        nvme0[0x14] = 0x00460001

        # 6. wait csts.rdy to 1
        while not (nvme0[0x1c]&0x1) == 1: pass

        # 7. identify controller
        nvme0.identify(d.Buffer(4096)).waitdone()

        # 8. create and identify all namespace
        nvme0.init_ns()

        # 9. set/get num of queues, 2 IO queues
        nvme0.setfeatures(0x7, cdw11=0x00010001).waitdone()
        nvme0.init_queues(nvme0.getfeatures(0x7).waitdone())

        # 10. send out all aer
        aerl = nvme0.id_data(259)+1
        for i in range(aerl):
            nvme0.aer()

    # 1. set pcie registers
    pcie.aspm = 0

    # 2. disable cc.en and wait csts.rdy to 0
    nvme0 = d.Controller(pcie, nvme_init_func=nvme_init)

    # test with ioworker
    nvme0n1 = d.Namespace(nvme0)
    qpair = d.Qpair(nvme0, 10)
    nvme0n1.ioworker(time=1).start().close()
    qpair2 = d.Qpair(nvme0, 10)
    with pytest.raises(d.QpairCreationError):
        qpair3 = d.Qpair(nvme0, 10)

    qpair.delete()
    qpair2.delete()
    nvme0n1.close()


def test_ioworker_op_dict_trim(nvme0n1):
    cmdlog_list = [None]*10000
    op_percentage = {2: 40, 9: 30, 1: 30}
    nvme0n1.ioworker(io_size=8,
                     io_count=10000,
                     op_percentage=op_percentage,
                     output_cmdlog_list=cmdlog_list).start().close()

    op_log = [c[2] for c in cmdlog_list]
    for op in (2, 9, 1):
        logging.info("occurance of %d: %d" % (op, op_log.count(op)))


def test_ioworker_io_sequence_read_write_trim_flush_uncorr(nvme0n1):
    cmd_seq = [(000000, 1, 0, 8),  #L2
               (200000, 2, 3, 1),
               (400000, 1, 2, 1),
               (600000, 9, 1, 1),
               (800000, 4, 0, 8),
               (1000000, 0, 0, 0)]
    cmdlog_list = [None]*len(cmd_seq)  #L8

    r = nvme0n1.ioworker(io_sequence=cmd_seq,  #L10
                         output_cmdlog_list=cmdlog_list).start().close()

    assert r.mseconds > 1000  #L13
    assert cmdlog_list[-1][2] == 0  #L14
    assert cmdlog_list[-2][2] == 4
    assert cmdlog_list[-3][2] == 9
    assert cmdlog_list[-4][2] == 1
    assert cmdlog_list[-5][2] == 2
    assert cmdlog_list[-6][2] == 1


def test_aer_with_multiple_sanitize(nvme0, nvme0n1, buf):  #L8
    if nvme0.id_data(331, 328) == 0:  #L9
        pytest.skip("sanitize operation is not supported")  #L10

    logging.info("supported sanitize operation: %d" % nvme0.id_data(331, 328))

    for i in range(3):
        nvme0.sanitize().waitdone()  #L13

        # check sanitize status in log page
        with pytest.warns(UserWarning, match="AER notification is triggered"):
            nvme0.getlogpage(0x81, buf, 20).waitdone()  #L17
            while buf.data(3, 2) & 0x7 != 1:  #L18
                time.sleep(1)
                nvme0.getlogpage(0x81, buf, 20).waitdone()  #L20
                progress = buf.data(1, 0)*100//0xffff
                logging.info("%d%%" % progress)


def test_verify_partial_namespace(nvme0):
    region_end=1024*1024*1024//512  # 1GB space
    nvme0n1 = d.Namespace(nvme0, 1, region_end)
    assert True == nvme0n1.verify_enable(True)

    nvme0n1.format()
    nvme0n1.ioworker(io_size=8,
                     lba_random=True,
                     region_end=region_end,
                     read_percentage=50,
                     time=30).start().close()
    nvme0n1.close()


def test_jsonrpc_list_qpairs(pciaddr):
    import json
    import socket

    # create the jsonrpc client
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect('/var/tmp/pynvme.sock')

    def jsonrpc_call(sock, method, params=[]):
        # create and send the command
        req = {}
        req['id'] = 1234567890
        req['jsonrpc'] = '2.0'
        req['method'] = method
        req['params'] = params
        sock.sendall(json.dumps(req).encode('ascii'))

        # receive the result
        resp = json.loads(sock.recv(4096).decode('ascii'))
        assert resp['id'] == 1234567890
        assert resp['jsonrpc'] == '2.0'
        return resp['result']

    result = jsonrpc_call(sock, 'list_all_qpair')
    assert len(result) == 0

    # create controller and admin queue
    pcie = d.Pcie(pciaddr)
    nvme0 = d.Controller(pcie)

    result = jsonrpc_call(sock, 'list_all_qpair')
    assert len(result) == 1
    assert result[0]['qid']-1 == 0

    result = jsonrpc_call(sock, 'list_all_qpair')
    assert len(result) == 1
    assert result[0]['qid']-1 == 0

    q1 = d.Qpair(nvme0, 8)
    result = jsonrpc_call(sock, 'list_all_qpair')
    assert len(result) == 2
    assert result[0]['qid']-1 == 0
    assert result[1]['qid']-1 == 1

    q2 = d.Qpair(nvme0, 8)
    result = jsonrpc_call(sock, 'list_all_qpair')
    assert len(result) == 3
    assert result[0]['qid']-1 == 0
    assert result[1]['qid']-1 == 1
    assert result[2]['qid']-1 == 2

    q1.delete()
    result = jsonrpc_call(sock, 'list_all_qpair')
    assert len(result) == 2
    assert result[0]['qid']-1 == 0
    assert result[1]['qid']-1 == 2

    q2.delete()
    result = jsonrpc_call(sock, 'list_all_qpair')
    assert len(result) == 1
    assert result[0]['qid']-1 == 0

    pcie.close()
    result = jsonrpc_call(sock, 'list_all_qpair')
    assert len(result) == 0


def test_powercycle_with_qpair(nvme0, nvme0n1, buf, subsystem):
    print(subsystem)
    qpair = d.Qpair(nvme0, 16)
    nvme0n1.write(qpair, buf, 0).waitdone()
    nvme0n1.read(qpair, buf, 0).waitdone()

    # delete qpair before power cycle, and then reset controller, recreate qpair
    qpair.delete()
    subsystem.power_cycle(10)
    nvme0.reset()
    qpair = d.Qpair(nvme0, 16)

    nvme0n1.read(qpair, buf, 0).waitdone()
    qpair.delete()


def test_reset_time(pcie):
    def nvme_init(nvme0):
        logging.info("user defined nvme init")

        nvme0[0x14] = 0
        while not (nvme0[0x1c]&0x1) == 0: pass
        logging.info(time.time())

        # 3. set admin queue registers
        nvme0.init_adminq()
        logging.info(time.time())

        # 5. enable cc.en
        nvme0[0x14] = 0x00460001

        # 6. wait csts.rdy to 1
        while not (nvme0[0x1c]&0x1) == 1: pass
        logging.info(time.time())

        # 7. identify controller
        nvme0.identify(d.Buffer(4096)).waitdone()
        logging.info(time.time())

        nvme0.setfeatures(0x7, cdw11=0x00ff00ff).waitdone()
        nvme0.init_queues(nvme0.getfeatures(0x7).waitdone())

    logging.info("1: nvme init")
    logging.info(time.time())
    nvme0 = d.Controller(pcie, nvme_init_func=nvme_init)
    subsystem = d.Subsystem(nvme0)

    qpair = d.Qpair(nvme0, 10)
    qpair2 = d.Qpair(nvme0, 10)
    qpair3 = d.Qpair(nvme0, 10)
    qpair.delete()
    qpair2.delete()
    qpair3.delete()

    logging.info("2: nvme reset")
    logging.info(time.time())
    nvme0.reset()

    logging.info("3: power cycle")
    subsystem.poweroff()
    logging.info(time.time())
    subsystem.poweron()
    nvme0.reset()


@pytest.mark.parametrize("ps", range(1, 5, 1))
def test_power_state_transition(pcie, nvme0, nvme0n1, qpair, buf, ps):
    # for accurate sleep delay
    import ctypes
    libc = ctypes.CDLL('libc.so.6')

    # write data to LBA 0x5a
    nvme0n1.write(qpair, buf, 0x5a).waitdone()

    # enable ASPM and get original power state
    pcie.aspm = 2
    orig_ps = nvme0.getfeatures(0x2).waitdone()

    # test with delay 1us-1ms
    for i in range(1000):
        # fix on power state 0 before test
        nvme0.setfeatures(0x2, cdw11=0).waitdone()
        libc.usleep(1000)

        # change power status
        nvme0.setfeatures(0x2, cdw11=ps)
        libc.usleep(i)

        # read lba 0x5a and verify data
        nvme0n1.read(qpair, buf, 0x5a).waitdone()
        assert buf[0] == 0x5a

        # consume the cpl of setfeatures above
        nvme0.waitdone()  # for setfeautres above

    # recover to original power state
    pcie.aspm = 0
    nvme0.setfeatures(0x2, cdw11=orig_ps).waitdone()


@pytest.mark.parametrize("nsid", [0, 1, 0xffffffff])
def test_getlogpage_nsid(nvme0, buf, nsid):
    logging.info("model name: %s, nsid %d" % (nvme0.id_data(63, 24, str), nsid))
    nvme0.getlogpage(0xCA, buf, 512, nsid=nsid).waitdone()
    nvme0.getlogpage(0x02, buf, 512, nsid=nsid).waitdone()


def test_ioworker_with_temperature(nvme0, nvme0n1, buf):
    with nvme0n1.ioworker(io_size=256,
                          time=30,
                          op_percentage={0:10,  # flush
                                         2:60,  # read
                                         9:30}), \
         nvme0n1.ioworker(io_size=8,
                          time=30,
                          op_percentage={0:10,  # flush
                                         9:10,  # trim
                                         1:80}):# write
        for i in range(40):
            time.sleep(1)
            nvme0.getlogpage(0x02, buf, 512).waitdone()
            ktemp = buf.data(2, 1)
            from pytemperature import k2c
            logging.info("temperature: %0.2f degreeC" %
                         k2c(ktemp))


def test_ioworker_jedec_enterprise_workload_512(nvme0n1):
    distribution = [1000]*5 + [200]*15 + [25]*80
    iosz_distribution = {1: 4,
                         2: 1,
                         3: 1,
                         4: 1,
                         5: 1,
                         6: 1,
                         7: 1,
                         8: 67,
                         16: 10,
                         32: 7,
                         64: 3,
                         128: 3}

    output_percentile_latency = dict.fromkeys([99, 99.99, 99.9999])
    nvme0n1.ioworker(io_size=iosz_distribution,
                     lba_random=True,
                     qdepth=128,
                     distribution = distribution,
                     read_percentage=0,
                     ptype=0xbeef, pvalue=100,
                     time=30,
                     output_percentile_latency=\
                       output_percentile_latency).start().close()
    logging.info(output_percentile_latency)
