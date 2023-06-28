
repository='dev_autotrade'
#repository='prod_audotrade'

#func='bestk'
func='endprice'

version='1'

ecr_login='aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 501587125031.dkr.ecr.ap-northeast-2.amazonaws.com'
build='docker build -t '+repository+':'+func+'.'+version+' .'
tag='docker tag '+repository+':'+func+'.'+version+' 501587125031.dkr.ecr.ap-northeast-2.amazonaws.com/'+repository+':'+func+'.'+version
push='docker push 501587125031.dkr.ecr.ap-northeast-2.amazonaws.com/'+repository+':'+func+'.'+version

print(ecr_login)
print(build)
print(tag)
print(push)

