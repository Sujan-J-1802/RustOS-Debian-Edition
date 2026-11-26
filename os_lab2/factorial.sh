#!/bin/bash
echo "Enter a Number: "
read n
if ! [[ "$n" =~ ^[0-9]+$ ]] || (( n > 20 ))
then
	echo "Enter an integer between 0 and 20"
	exit 1
fi
p=1
i=1
while (( i <= n))
do
	p=$((p * i))
	i=$((i + 1))
done
echo "The Factorial of the given Number is $p"
