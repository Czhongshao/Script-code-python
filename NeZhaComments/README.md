# 需要注意到的点

## 一、爬虫部分

### 1.Cookie

因为网站的数据时常会进行更新，此时若是再执行爬虫代码，需要更新Cookie的参数设置
可以先运行第一个爬虫代码块，看看效果
___

## 二、Hadoop

这一部分基于Ubuntu22.04进行部署

### 基于Linux的Hadoop伪分布式安装

#### hadoop用户设置

1. 创建新用户hadoop

    ```bash
        su root

        adduser hadoop
        
        # 切换到hadoop用户
        su hadoop

        # 在root用户阶段，执行visudo 修改配置
        su root
        
        # 该命令打开的是/etc/sudoers文件
        visudo

        # 在root ALL=(ALL:ALL) ALL下一行添加下述内容
        hadoop ALL=(ALL:ALL) ALL

        # 退出root用户
        exit
    ```

2. 安装ssh

    ```bash
        # 1. 更新apt源
        sudo apt-get update

        # 2. 安装ssh并且启动服务端
        sudo apt-get install openssh-server
        sudo service ssh start

        # 3. 登录本机(依次输入yes、密码)
        ssh localhost
        
        # 4. 退出ssh
        exit

        # 5. ssh免密登录
        cd ~/.ssh/

        #【多步骤版本，一路回车即可】
        ssh-keygen -t rsa
        #【一步到位版本】
        ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

        # 6. 添加密钥到授权当中
        cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

        # 7. 尝试直接登陆
        ssh localhost
    ```

3. 安装vim

    ```bash
        sudo apt-get install vim
    ```

4. 安装JDK并配置环境变量

    ```bash
        # 1. 安装openjdk-8-jdk
        sudo apt-get install openjdk-8-jdk

        # 2. 查看java路径与版本
        echo $JAVA_HOME
        java -version
        whereis java

        # 3. 更改JDK安装路径为上述部分
        ##【vim: 键入i，即可插入删除内容；按esc退出插入状态；键入  :wq  后回车，退出并保存更改】
        vim ~/.bashrc

        # 4. 使环境变量生效
        source ~/.bashrc
    ```

    输入的环境变量

    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
    export JRE_HOME=${JAVA_HOME}/jre
    export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
    export PATH=${JAVA_HOME}/bin:$PATH
    ```

5. 安装Hadoop - 3.3.6

    - hadoop 安装

    ```bash
        # 方法1: 使用命令行下载（比较缓慢）
        wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
        
        # 方法2: 现在本地windows下载，然后通过xshell传输给ubuntu服务器
        1. 详细方法请搜索：`https://blog.csdn.net/m0_70885101/article/details/127291049` 
        2. 这里提供必要的指令
            1. Ubuntu 服务器当中查询
            `hostname -I`: 查询服务器的IP地址
            2. xshell 安装必要包
            `sudo apt-get install -y lrzsz`: 安装上传文件的包
            3. 上传文件
            `rz -E`: tips: 若是报错，是因为大文件需要使用`rz -be`进行上传
    ```

    - 解压

    ```bash
        # 查询当前压缩包文件名称
        hadoop@ZhongShao:~$ ls
        hadoop-3.3.6.tar.gz
    ```

    ```bash
        # 解压到/usr/local路径下
        sudo tar -zxf ~/hadoop-3.3.6.tar.gz -C /usr/local
        cd /usr/local

        # 更改文件名为hadoop
        sudo mv ./hadoop-3.3.6/ ./hadoop

        # 修改文件权限
        sudo chown -R hadoop ./hadoop

    ```

    - 配置环境变量

    ```bash
        # 配置环境变量
        vim ~/.bashrc
        
        # HADOOP VARIABLES START 
        export HADOOP_INSTALL=/usr/local/hadoop
        export PATH=$PATH:$HADOOP_INSTALL/bin
        export PATH=$PATH:$HADOOP_INSTALL/sbin
        export HADOOP_MAPRED_HOME=$HADOOP_INSTALL 
        export HADOOP_COMMON_HOME=$HADOOP_INSTALL 
        export HADOOP_HDFS_HOME=$HADOOP_INSTALL 
        export YARN_HOME=$HADOOP_INSTALL 
        export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_INSTALL/lib/native
        export HADOOP_OPTS="-Djava.library.path=$HADOOP_INSTALL/lib"
        #HADOOP VARIABLES END 

        # 更新环境变量
        srouce ~/.bashrc

        # 查看hadoop是否可用
        hadoop version
    ```

    - hadoop 伪分布式配置

    ```bash
        cd /usr/lcoal/hadoop

        # 1. 配置 hadoop-env.sh
        vim ./etc/hadoop/hadoop-env.sh

        # The java implementation to use. 
        export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
        export HADOOP=/usr/local/hadoop
        export PATH=$PATH:/usr/local/hadoop/bin

        # 2. 配置 yarn-env.sh
        vim ./etc/hadoop/yarn-env.sh

        # export JAVA_HOME
        JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
        ___

        # 3. 配置 core-site.xml 
        vim ./etc/hadoop/core-site.xml

        <configuration>
            <property>
                <name>hadoop.tmp.dir</name>
                <value>file:/usr/local/hadoop/tmp</value>
                <description>A base for other temporary directories.</description>
            </property>
            <property>
                <name>fs.defaultFS</name>
                <value>hdfs://localhost:9000</value>
            </property>
        </configuration>

        # 4. 配置 hdfs-site.xml
        vim ./etc/hadoop/hdfs-site.xml

        <configuration>
            <property>
                <name>dfs.replication</name>
                <value>1</value>
            </property>
            <property>
                <name>dfs.namenode.name.dir</name>
                <value>file:/usr/local/hadoop/tmp/dfs/name</value>
            </property>
            <property>
                <name>dfs.datanode.data.dir</name>
                <value>file:/usr/local/hadoop/tmp/dfs/data</value>
            </property>
        </configuration>

        # 5. 配置 yarn-site.xml
        vim ./etc/hadoop/yarn-site.xml

        <configuration> 
        <!-- Site specific YARN configuration properties -->
            <property> 
                <name>yarn.nodemanager.aux-services</name> 
                <value>mapreduce_shuffle</value> 
            </property> 
            <property> 
                <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name> 
                <value>org.apache.hadoop.mapred.ShuffleHandler</value> 
            </property> 
            <property> 
                <name>yarn.resourcemanager.address</name> 
                <value>127.0.0.1:8032</value> 
            </property> 
            <property> 
                <name>yarn.resourcemanager.scheduler.address</name> 
                <value>127.0.0.1:8030</value> 
            </property> 
            <property> 
                <name>yarn.resourcemanager.resource-tracker.address</name> 
                <value>127.0.0.1:8031</value> 
            </property> 
        </configuration>
    ```

    - 重启检验是否配置成功

    ```bash
        sudo reboot
        # 或者
        sudo shutdown -r now
        # 在WSL2当中，需要在本地终端当中关闭Ubuntu实例后再打开
        wsl --shutdown
    ```

    ```bash
        # 注意此时请切换到对应用户下
        su hadoop
        # 切换到工作文件夹下（非必要）
        cd /usr/local
        # 检验hadoop安装是否成功
        hadoop version
    ```

    - 启动HDFS伪分布式模式

    ```bash
        # 1. 启动ssh
        sudo service ssh start
        # 2. 格式化namenode(只执行一次即可，若是重复执行，需要参考下述部分的tips)
        hdfs namenode -format
        # 3. 启动hdfs
        start-all.sh
        ## 或
        start-dfs.sh
        start-yarn.sh
        # 4. 进程查询
        jps
        # 5. 结束指令
        stop-all.sh
        ## 或
        stop-dfs.sh
        stop-yarn.sh

        *正常应该有六个进程*
        4533 Jps
        3049 DataNode
        2826 NameNode
        3307 SecondaryNameNode
        4172 NodeManager
        3774 ResourceManager
        ## tips: 若缺失DataNode：(https://blog.csdn.net/qq_45069279/article/details/111559319) (https://blog.csdn.net/donoot/article/details/109777398)

        # 5. 打开浏览器查看
        http://localhost:9870/

        http://localhost:8088/
    ```

___

## 三、HBase

### 安装HBase - 2.6.2

- **下载压缩包**

    ```bash
        # 方法1：windows本地下载后通过xshell传输给ubuntu服务器
        **清华大学镜像站：(https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/)**

        # 方法2：通过指令下载到/home/hadoop路径下，需要先进入hadoop用户
        cd ~
        pwd
        # hadoop@ZhongShao:~$ pwd
        # /home/hadoop

        wget https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/2.6.2/hbase-2.6.2-bin.tar.gz
    ```

- **解压文件**

    ```bash
        # 解压到/usr/local路径下
        sudo tar -zxf ~/hbase-2.6.2-bin.tar.gz -C /usr/local
        cd /usr/local

        # 更改文件名为hbase
        sudo mv ./hbase-2.6.2/ ./hbase

        # 更改HBase权限
        sudo chown -R hadoop ./hbase
    ```

- **编辑环境变量**

    ```bash
        # 编辑配置文件
        sudo vim ~/.bashrc
        
        # HBASE
        export PATH=$PATH:/usr/local/hbase/bin

        # 更新环境变量
        source ~/.bashrc
    ```

- **HBase伪分布模式设置**

    ```bash
        # HBase有三种运行模式，单机模式、伪分布模式、分布式模式。
        ## 需要以下条件
        JDK
        Hadoop (伪分布式模式需要) 
        SSH
    ```

    ```bash
        # 0. 复制 htrace 的 jar 包到 hbase 的 lib 路径下 (https://blog.csdn.net/Y_6155/article/details/110455338)
        cp /usr/local/hbase/lib/client-facing-thirdparty/htrace-core4-4.1.0-incubating.jar /usr/local/hbase/lib/

        # 1. 配置 hbase-env.sh
        vim /usr/local/hbase/conf/hbase-env.sh

        #JAVA
        export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
        export HBASE_CLASSPATH=/usr/local/hadoop/conf
        export HBASE_MANAGES_ZK=true

        #Not Use Norm Zookpeer
        export HBASE_DISABLE_HADOOP_CLASSPATH_LOOKUP="true"

        # 2. 配置 hbase-site.xml
        vim /usr/local/hbase/conf/hbase-site.xml

        1. 修改hbase.rootdir，指定HBase数据在HDFS上的存储路径
        2. 将属性hbase.cluter.distributed设置为true
        3. 假设当前Hadoop集群运行在伪分布式模式下，在本机上运行，且NameNode运行在9000端口
        4. 设置Zookeeper状态
        5. 配置Thrift服务

        <configuration>
            <!-- 定义HBase是否以分布式模式运行 -->
            <property>
                <name>hbase.cluster.distributed</name>
                <value>true</value>
            </property>
            
            <!-- HBase数据的HDFS根目录 -->
            <property>
                <name>hbase.rootdir</name>
                <value>hdfs://localhost:9000/hbase</value>
            </property>
            
            <!-- HBase使用的ZooKeeper集群的主机名列表 -->
            <property>
                <name>hbase.zookeeper.quorum</name>
                <value>localhost</value>
            </property>
            
            <!-- ZooKeeper客户端端口 -->
            <property>
                <name>hbase.zookeeper.property.clientPort</name>
                <value>2181</value>
            </property>
            
            <!-- Thrift服务的监听地址 -->
            <property>
                <name>hbase.thrift.bind.address</name>
                <value>localhost</value>
            </property>
            
            <!-- Thrift服务的监听端口 -->
            <property>
                <name>hbase.thrift.port</name>
                <value>9090</value>
            </property>
        </configuration>

        # 3. 测试运行HBase
            # 1. 切换到 hadoop 用户
            su hadoop
            # 2. 登陆ssh
            sudo service ssh start
            ssh localhost
            # 3. 启动 Hadoop 分布式文件系统（HDFS）的守护进程
            start-dfs.sh
            ## jps 查看进程
            1304 DataNode              # 管理文件系统的元数据，负责文件和目录的命名空间
            1578 SecondaryNameNode     # 辅助 NameNode，定期合并编辑日志和文件系统镜像，减轻 NameNode 的负担
            1087 NameNode              # 存储实际的数据块，负责数据的存储和读取

            # 4. 启动 YARN 的守护进程
            start-yarn.sh
            ## jps 查看进程
            2373 NodeManager           # 运行在每个节点上，管理单个节点的资源和任务
            2173 ResourceManager       # 管理集群资源，负责资源的分配和调度

            # 6. 启动hbase
            start-hbase.sh
            ## jps 查看进程
            5536 HRegionServer         # 负责管理 Region，处理客户端的读写请求，确保数据的存储和读取
            5160 HQuorumPeer           # 作为 ZooKeeper 的部分，提供分布式协调服务，管理员数据，监控节点状态，确保集群的高可用性和一致性
            5342 HMaster               # 作为 Hbase的主节点，管理原数据，分配 Region，监控集群状态，确保集群的正常运行和高可用性
            9146 ThriftServer          # 启动 Thrift 服务器，通过 Thrift 协议提供 HBase 的接口

            # 若是服务未启动，需要额外启动
            # 启动 thrift、regionserver 服务
            hbase-daemon.sh start thrift
            hbase-daemon.sh start regionserver

            ## tips: 出现报错如下

            `SLF4J: Class path contains multiple SLF4J bindings.`
            `SLF4J: Found binding in [jar:file:/usr/local/hbase/lib/client-facing-thirdparty/log4j-slf4j-impl-2.17.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]`
            `SLF4J: Found binding in [jar:file:/usr/local/hadoop/share/hadoop/common/lib/slf4j-reload4j-1.7.36.jar!/org/slf4j/impl/StaticLoggerBinder.class]`
            `SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.`
            `SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]`

            ## 为jar包冲突情况
            
            移除`slf4j-reload4j-1.7.36.jar`即可
            sudo rm /usr/local/hadoop/share/hadoop/common/lib/slf4j-reload4j-1.7.36.jar
    ```

## 四、配置Miniconda

### 安装 Miniconda - 222

- **配置conda环境变量**

```bash
    # 切换到对应用户
    su hadoop

    # 编辑环境变量
    vim ~/.bashrc

    # <<< conda initialize <<<
    export PATH=/home/zhongshao/miniconda3/bin:$PATH

    # 更新环境变量
    source ~/.bashrc

```


