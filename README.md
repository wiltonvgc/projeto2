# Projeto 2 - Experiências de Roteamento com Mininet

**Grupo 9**

	Bruno Murari Lucas
	Thiago Arraiol Casaes
	Wilton Vicente Gonçalves da Cruz    
  
## Laboratórios utilizados:

 * [Lab 1: Configuração Básica de Roteadores Cisco](https://github.com/wiltonvgc/projeto2/blob/master/relatorio.mdown#laboratório-1)
 * [Lab 2: Configuração de Roteamento Estático](https://github.com/wiltonvgc/projeto2/blob/master/relatorio.mdown#laboratório-2)
 * [Lab 3: Configuração de Roteamento Dinâmico](https://github.com/wiltonvgc/projeto2/blob/master/relatorio.mdown#laboratório-3)
 * [Dificuldades encontradas](https://github.com/wiltonvgc/projeto2/blob/master/relatorio.mdown#diiculdades-econtradas)
 * [Resultados](https://github.com/wiltonvgc/projeto2/blob/master/relatorio.mdown#resultados)
 * [Referências](https://github.com/wiltonvgc/projeto2/blob/master/relatorio.mdown#referências)


## Laboratório 1

### Topologia:
![Imagem Topologia1](/lab1/lab1-Prints/Topologia%20Lab1.jpg)


### Breve Explicação do Código
  Definição dos equipamentos de rede e suas ligações. Note que o **PC-PT Terminal** não é inserido por se tratar apenas de um console utilizado para configurar o roteador. 
```python
class Topologia(Topo):
   
    def __init__(self):
    super(Topologia, self ).__init__()
    n1 = self.addNode('pc1')				#host pc1
	n2 = self.addNode('pc2')				#host pc2
	s0 = self.addSwitch('s0')				#switch
	self.addLink(n1,s0)						#link pc1 to s0
	self.addLink(n2,s0)						#link pc2 to s0
	r0 = self.addSwitch('r0',type='Router')	#roteador r0
	self.addLink(r0,s0)						#link switch to router
	return
``` 

Comandos usados no Mininet
```python
 os.system("rm -f /tmp/R*.log /tmp/R*.pid logs/*")
 os.system("mn -c >/dev/null 2>&1")
    
 net = Mininet(topo=Topologia())
 net.start()
```

Indica que o **IP Forward** está ativo 
 ```python
 #Seta roteador r0
    for router in net.switches:
	if(router.name=='r0'):
        	router.cmd("sysctl -w net.ipv4.ip_forward=1")
        	router.waitOutput() 
 ```

Configura o roteador `r0` usando Zebra
 ```python
 for router in net.switches:
        if(router.name == 'r0'):
       		router.cmd("/usr/lib/quagga/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (router.name, router.name, router.name))
        	router.waitOutput() 
 ```

Configura interfaces dos hosts indicando o **Default Gateway** com o **IP** do **Roteador** 
```python
  for host in net.hosts:
	host.cmd("ifconfig %s-eth0 %s" % (host.name, getIP(host.name)))
    	host.cmd("route add default gw %s" % '192.168.0.254')
```

## Laboratório 2
### Topologia:
![Imagem Topologia2](/lab2/lab2-Prints/Topologia%20Lab2.jpg)

### Breve Explicação do Código [`lab2.py`](/lab2/lab2.py):
Configura as interfaces dos roteadores `rA`e `rB`com **zebra**
```python
for router in net.switches:
        if(router.name=='r1' or router.name=='r2'):
       		router.cmd("/usr/lib/quagga/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (router.name, router.name, router.name))
        	router.waitOutput()
```
### Breve Explicação dos Código de Configuração [`zebra.conf`](/lab2/conf/)
As interfaces dos roteadores são definidas nos arquivos de configuração do zebra.
No trecho abaixo os atributos da interface `eth1` do roteador `r1` são definidos
```
interface r1-eth1
  ip address 192.168.1.254/24
```
Assim como as rotas
```
ip route 192.168.1.0/24 192.168.1.1
ip route 192.168.1.0/24 192.168.1.2
ip route 192.168.2.0/24 192.168.2.1
ip route 192.168.2.0/24 192.168.2.2
ip route 192.168.3.0/24 192.168.3.1
ip route 192.168.3.0/24 192.168.3.2
```


## Laboratório 3
### Topologia:
![Imagem Topologia3](/lab3/lab3-Prints/Topologia%20lab3.jpg)

### Breve Explicação do Código [`lab3.py`](/lab3/lab3.py):
Nos roteadores `r1`, `r2` e `r3` além do arquivo **zebra** o **bgpd** também é utilizado para o roteamento estático. 
```python
for router in net.switches:
        if(router.name=='r2' or router.name=='r1' or router.name=='r3'):
          router.cmd("/usr/lib/quagga/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (router.name, router.name, router.name))
          router.waitOutput()
    router.cmd("/usr/lib/quagga/bgpd -f conf/bgpd-%s.conf -d -i /tmp/bgp-%s.pid > logs/%s-bgpd-stdout 2>&1" % (router.name, router.name, router.name), shell=True)
          router.waitOutput()
``` 

### Breve Explicação dos arquivos de [`configuração`](/lab3/conf)
Além dos arquivos que definem as interfaces em zebra (também usados no [Lab2](/lab2/conf/)), arquivos de configuração do **bgpd** também são utilizados para criar a tabela de roteamento de cada roteador.
Nesse trecho do arquivo [`bgpd-r1.conf`](/lab3/conf/bgpd-r1.conf) os vizinhos são inseridos.  
```
router bgp 1
  bgp router-id 172.16.11.254
  network 172.16.10.0/24
  neighbor 172.16.10.1 remote-as 2
    neighbor 172.16.10.1 ebgp-multihop
    neighbor 172.16.10.1 next-hop-self
    neighbor 172.16.10.1 timers 5 5
  neighbor 172.16.10.2 remote-as 2
    neighbor 172.16.10.2 ebgp-multihop
    neighbor 172.16.10.2 next-hop-self
    neighbor 172.16.10.2 timers 5 5
```
## Dificuldades Encontradas
* Relatório no formato GitHub MarkDown. Foi necessário aprender a sintaxe já que não sabíamos usar esse formato. Para isso utilizamos a documentação [oficial](https://guides.github.com/features/mastering-markdown/) e a ferramenta [MarkDown Editor](https://jbt.github.io/markdown-editor/).

## Resultados
##Laboratório 1
Alguns exemplos de testes feitos podem ser vistos abaixo. Imagens com *prints* de todos os testes podem ser encontradas nas pasta [lab1-Prints](/lab1/lab1-Prints/) 
### Dump
![Imagem Dump](https://github.com/wiltonvgc/projeto2/blob/master/lab1/lab1-Prints/dump.png)

### Ping de `pc1` para `pc2`
![Imagem ping pc1 pc2](https://github.com/wiltonvgc/projeto2/blob/master/lab1/lab1-Prints/pc1ToPc2.png)

### Ping do Roteador `r0` para `pc2`
![Imagem ping r0 pc2](https://github.com/wiltonvgc/projeto2/blob/master/lab1/lab1-Prints/RouterToPc2.png) 

### Rota do Roteador `r0`
![Imagem rota r0](https://github.com/wiltonvgc/projeto2/blob/master/lab1/lab1-Prints/routeR0.png)

## Laboratório 2
### Ping All
Usado para testar o *ping* de todos os equipamentos entre si.
![Imagem pingall](https://github.com/wiltonvgc/projeto2/blob/master/lab2/lab2-Prints/pingallLab2.png)

## Laboratório 3
### Ping All
![Imagem pingall3](https://github.com/wiltonvgc/projeto2/blob/master/lab3/lab3-Prints/pingall.png)

### Roteador RJ `r2` BGP
![Imagem pingall](https://github.com/wiltonvgc/projeto2/blob/master/lab3/lab3-Prints/RoteadorRJ_BGP.png)

### Roteador SP `r1` BGP
![Imagem pingall](https://github.com/wiltonvgc/projeto2/blob/master/lab3/lab3-Prints/RoteadorSP_BGP.png)

### Roteador BH `r3` BGP
![Imagem pingall](https://github.com/wiltonvgc/projeto2/blob/master/lab3/lab3-Prints/RoteadorBH_BGP.png)

## Referências
* Imagens geradas com o software [Cisco Packet Tracer e os labs de demonstração](http://labcisco.blogspot.com.br/p/laboratorios.html)
* [Máquinas Virtuais](http://mininet.org/download/) com Mininet já instalado 
* Apoio ao uso de [Quagga](http://www.nongnu.org/quagga/docs/docs-info.html#Interface-Commands)

