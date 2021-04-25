

1. 분석에 사용할 jar파일을 준비한다. (예를 들어 http://www.java2s.com/ 와 같은 곳에서 다운 받을 수 있다.)

2. 다운 받은 jar파일로 분석을 돌려본다. 예를 들어 http://www.java2s.com/Code/Jar/a/Downloadabbot0130jar.htm 에서 zeus-3.5.jar를 받았다고 했을때 다음과 같은 커맨드를 입력하면 된다

    $ ./run -jre1.6 -phantom context-insensitive zeus-3.5.jar

3. 분석이 잘 끝나는지 확인한다. (만약 분석이 제대로 안돌아갈 경우 다른 jar프로그램을 찾자)
분석이 잘 끝났을 경우 아래와 같이 분석 결과가 출련되어야 한다. 분석 결과에서 아래와 같이 reachable application casts가 0이 아니어야 한다. 0일 경우 분석이 제대로 안돌아간 것이다.

-----------------------------------------------------------
Client results:
    number of FPG edges                  2,084,060
    reachable casts                      4,533
    #may-fail casts                      3,300
    reachable application casts          420
    #Application may-fail casts          376
    reachable virtual call sites         45,313
    #poly call sites                     3,870
    var points-to                        22,612,625 (insens) / 22,612,625 (sens)
    regular call graph edges             103,609
    reflective call graph edges          7,028
    #call graph edges                    110,637
    reachable methods                    19,488 (insens) / 19,488 (sens)
-----------------------------------------------------------


4. 아래의 커맨드를 실행시켜 해당 프로그램의 GTT를 구한다. (매우 오래 걸린다.)

    $ python learn_minimal.py zeus-3.5.jar

GTT는 Minimal_Abstraction.fact에 저장 된다.

5. GTT로 프로그램을 돌리기 위해선 아래와 같이 하면 된다.

(1) $ python alloc_to_facts.py alloc Minimal_Abstractin.facts

(2) $ ./run -jre1.6 -phantom -heap-abstraction HeapAbstraction.myfacts 3-object-sensitive+2-heap zeus-3.5.jar

다른 프로그램을 분석 할 경우 zeus-3.5.jar 자리에 분석할 프로그램을 넣어주면 된다.

