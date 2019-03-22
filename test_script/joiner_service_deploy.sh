#!/bin/sh
branchname=$1
echo ${branchname}

/data/webapps/liping.liu/*/bin/join_server.sh stop

cd /data/webapps/liping.liu
rm -rf search-joiner*

cd /data/webapps/liping.liu/joiner

git checkout master
git branch -D ${branchname}
git checkout ${branchname}
git pull origin ${branchname}


mvn clean package

cd  /data/webapps/liping.liu/*/target
cp search-joiner-core-*-release.tar.gz /data/webapps/liping.liu/


cd /data/webapps/liping.liu/
tar -zxvf search-joiner-core-*-release.tar.gz
rm -rf search-joiner-core-*-release.tar.gz
mv search-joiner-core* search-joiner-core-liping


cd search-joiner-core-liping

sed -i.bak 's#<Apps description=.*</Apps>#<Apps description="joiner应用加载的app">lipingtestmongo</Apps>#g' conf/configuration.xml
sed -i.bak 's/3333/4333/g' conf/configuration.xml
sed -i.bak 's/<CacheSource>/<CacheSource>searchMongoCluster2/g' conf/configuration.xml
sed -i.bak 's/<StartConsumer>true<\/StartConsumer>/<StartConsumer>false<\/StartConsumer>/g' conf/configuration.xml
sed -i.bak 's/<Open description="">true<\/Open>/<Open description="">false<\/Open>/g' conf/configuration.xml

#起服务
cd bin
./join_server.sh restart