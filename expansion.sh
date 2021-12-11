#!/bin/bash
#키워드 입력받고 동의어 Get
read -p "Enter the keyword > " keyword
eval "curl -s -XGET --header 'Content-Type: application/json' http://localhost:9200/paper1/_analyze -d '{\"analyzer\": \"search_synonyms\", \"text\": \"${keyword}\"}'" > analyze.json

data=`cat analyze.json | jq '.tokens[] | .token'`

echo 
echo "[$keyword의 동의어는]"
echo ${data[0]}
echo -e "\n" 
echo "[주의] _(underbar) 문자는 공백 문자로 대체하세요"
echo "질의 확장할 동의어를 입력하세요. 기존 검색어를 사용하려면 0 을 입력하세요"
read -p "keyword > " input

#만약 input에 공백이 있다면 %20으로 치환
input=${input/ /%20} 

#query
if [ "$input" = 0 ]
then
	eval "curl -s -XPOST  http://localhost:9200/paper1/_search?q=$keyword" > result.json
else
	eval "curl -s -XPOST  http://localhost:9200/paper1/_search?q=$input" > result.json	
fi

#query에 대한 결과를 parse 
top_rank=`cat result.json | jq '.hits.hits[] | ._source.title'`

echo "$top_rank" > a
readarray -t arr < a

score=`cat result.json | jq '.hits.hits[] | ._score'`
score_arr=(${score})
cnt=1

echo -e "\n\n"
echo "검색결과는 다음과 같습니다"
echo "--------------------------------------------"
for i in "${!arr[@]}"; do
    printf "$cnt. Title: %s \n    score: %s\n" "${arr[i]}" "${score_arr[i]}"
    cnt=$((cnt+1))
done	
