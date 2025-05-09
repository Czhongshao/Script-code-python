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

        # 2. 安装ssh服务端
        sudo apt-get install openssh-server

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
        # 检验hadoop安装是否成功
        hadoop version
    ```

    - 启动HDFS伪分布式模式

    ```bash
        # 1. 启动ssh
        sudo service ssh start
        # 2. 格式化namenode
        hdfs namenode -format
        # 3. 启动hdfs
        start-all.sh
        # 4. 进程查询
        jps
        # 5. 打开浏览器查看
        http://localhost:9870/
        
        http://localhost:8088/
    ```


`status`

___
