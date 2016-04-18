#!/usr/bin/python
# -*- coding: latin-1 -*-
# ^^^ needed, as otherwise pretty German Umlaute can't be used.

import sys

# Es wird eine Knoten-Klasse definiert, aus der der für den Aho-Corasick
# benötigte trie später gebaut wird.
class Node:
	# Bei der Initialisation werden ein paar wichtige Felder erstellt,
	# zum großen teil auf Null-Werte gesetzt. 
	def __init__(self):
		# Die fail-node (fnode) ist der Knoten, der vom Algorythmus
		# angesprungen wird, wenn sonst keine Transitionen zur verfügung
		# stehen. Dieser sollte nur bei der Baumwurzel self sein.
		self.fnode = self
		
		# Das Symbol, welches die Transition zu diesem Knoten bewirkt.
		self.symbol = None
		
                # Das Rating, das Einfluss darauf hat, welches Wort in der
                # Autokorrektur vorgeschlagen wird. Wird mit jedem Wort er-
                # höht, das durch diesen Knoten erreicht werden kann.
                self.rating = 0

		# Alle Knoten, die von diesem erreicht werden können.
		self.children = []
		
		# Wenn an diesem Knoten irgendwelche Matches passieren und ent-
		# sprechend Ausgaben vorgenommen werden müssen, werden die matches
		# hier gespeichert.
		self.matches = []

		# Jeder Knoten erhält eine ID. Diese wird später die Symbol-
		# folge sein, die benötigt wird, um zu diesem Knoten zu gelangen.
		# Nur die Wurzel hat 'None' als ID. 
		self.nid = None
	@classmethod
	def populated(cls, matches, fnode, symbol, string, rating):
		# Wir bauen auf einem zum größten Teil null-initialisierten
		# Knoten auf und fügen Informationen hinzu, um einen neuen,
		# nützlichen Knoten zu erstellen.
		self = cls()
		self.fnode = fnode
		self.symbol = symbol
		self.matches = matches
		self.nid = string
                self.rating = rating
		return self

	def addChild(self, node):
		self.children.append(node)

        def getChildWithMaxRating(self):
            childMaxRating = None
            maxRating = 0

            for child in self.children:
                if int(child.rating) > maxRating:
                    childMaxRating = child
                    maxRating = child.rating

            return childMaxRating
    
        # Add a score to the current rating. This happens every time, when
        # the automaton is getting build and a letter from the patterns list
        # matches an already existing letter.
        def addRating(self, score):
                self.rating = int(self.rating) + int(score)

	# hasChild prüft, ob ein Knoten ein child hat, welches mit dem gegebenen
	# Symbol angesprungen werden kann.
	def hasChild(self, symbol):
		for c in self.children:
			if c.symbol == symbol:
				return 1
		return 0
	
	# getChild returned den Kinderknoten, der mit dem gegebenen Symbol erreicht
	# werden kann. Falls es keinen entsprechenden Knoten gibt, returnen wir
	# einfach None.
	def getChild(self, symbol):
		for c in self.children:
			if c.symbol == symbol:
				return c
		return None
	
	# Eine Methode um ein neues Matching (-> Ausgabe) zu einem Knoten hinzu
	# zu fügen.
	def addMatch(self, match):
		self.matches.append(match)


# findFailureNode findet und returned den Knoten, der durch eine Failure-
# Transition erreicht wird, ausgehend von einem gegeben Knoten und dem Baum
# des Knotens.
def findFailureNode(node, startnode):
	# Wenn der Knoten von Interesse der Startknoten ist, ist der Startknoten
	# auch der Failknoten.
	if node.nid == None:
		return startnode
	
	# Ansonesten wird nun der längste postfix der string des Knotens von
	# Interesse gesucht, der auch ein prefix im trie ist. Der string eines
	# Knotens ist dabei die Symbolfolge, die benötigt wird, um zu dem Knoten
	# zu gelangen (bei der Wurzel angefangen). Dabei ist die ID des Knotens
	# (nid) praktischer Weise auch eben dieser string. Dabei werden die
	# möglichen postfixes vom Längsten angefangen durchprobiert. Somit kann
	# die Schleife abgebrochen werden, sobald ein postfix auch einem prefix
	# entspricht, da es dann automatisch der längste postfix ist.
	for i in range(1,len(node.nid)):
		subterm = node.nid[i:]
		curnode = startnode
		success = 1
		for c in subterm:
			child = curnode.getChild(c)
			if child == None:
				# Wenn kein Knoten mehr gefunden werden kann, ist
				# dieser postfix kein prefix und es kann zum Test
				# des nächsten postfixes übergegangen werden.
				success = 0
				break
			else:
				curnode = child
		if(success):
			# Hier landen wir, wenn die if-Kondition in der 2. for-
			# Schleife *nicht* eingetroffen ist. Das heißt, es wurde
			# ein Knoten gefunden, der mit dem aktuellen postfix er-
			# reicht werden kann => dies ist unsere failure node.
			return curnode
	
	# Es wurde keine failure node gefunden. Also ist die Wurzel unsere failure
	# node, da kein postfix des fragichen Eingabeknotens auch ein prefix im
	# trie ist.
	return startnode

# refreschAllFNodes verwendet findFailureNode um die failure nodes (bzw. Transitionen)
# aller Knoten im trie zu finden und zu aktualisieren. Dies funktiontiert selbstverständlich
# erst, wenn der Baum selbst bereits fertig gestellt ist.
def refreshAllFNodes(nodes, startnode):
	# We're doing a breadth-first search, so memorize all child
	# nodes of all current nodes in variable nextLevel to then
	# worry about those next.
	nextLevel = []
	
	# Wir iterieren über alle Knoten in dem aktuellen Level und suchen deren Failknoten.
	for node in nodes:
		nextLevel += node.children
		node.fnode = findFailureNode(node, startnode)
		node.matches += node.fnode.matches
	
	# Wenn es noch ein nächstes Level im trie gibt, rekursieren wir weiter und ver-
	# vollständigen die fnodes. Sonst sind wir fertig.
	if len(nextLevel) > 0:
		refreshAllFNodes(nextLevel, startnode)

# Eine Methode um den trie (einigermaßen) schön bzw. lesbar in stdout darzustellen.
# For debug purposes and curious people. But remember: curiosity killed the cat. Be careful.
def debug_print_trie(node, prefix):
	nodeIdString = "__root__" if node.nid == None else node.nid
	fnodeIdString = "__root__" if node.fnode.nid == None else node.fnode.nid
	print prefix + nodeIdString + ": " + str(node.symbol) + " " + str(node.matches) + " (" + fnodeIdString + ")"
	for c in node.children:
		debug_print_trie(c, prefix + "   ")




def buildAutomaton(patterns):
    # Zuerst wird der Automaton (Baum) gebaut.
    # Dazu wird erst ein Startknoten (Wurzel) erstellt.
    startnode = Node()

    # Jede string in unserer Pattern-Datei wird nun in den Baum eingefügt, ein Pattern
    # nach dem anderen.
    for p in patterns:
    
            score = p.split()[0]
            p = p.split()[1]
            
            # Wir beginnen immer an der Wurzel.
            curn = startnode
            # processedStr enthält die Zeichen, die bis zu dem aktuellen Punkt verwertet
            # bzw. verarbeitet wurden.
            processedStr = ""
            for c in p:
                    processedStr += c
                    child = curn.getChild(c)
                    if child != None:
                            # Die Transition, die für die aktuelle Position im Pattern
                            # nötig ist, existiert bereits. Wir können also die ent-
                            # sprechende Transition nehmen und brauchen sonst nichts
                            # zu unternehmen.
                            # Es muss noch das Rating erhöht werden.
                            child.addRating(score)
                            curn = child
                    else:
                            # Eine Transition existiert noch nicht. Also wird ein neuer
                            # Knoten erstellt, der dieser Transition entspricht.
                            newc = Node.populated([], startnode, c, processedStr, score)
                            # Wir müssen den neuen Knoten in den Baum einfügen, nämlich
                            # als Kind des aktuellen.
                            curn.addChild(newc)
                            # Schließlich ist es möglich, weiter im Baum fortzufahren.
                            curn = newc
                    if processedStr == p:
                            # Wenn die Zeichen, die bisher verarbeitet wurden, dem Pattern
                            # entsprechen, haben wir ein Match an dem aktuellen Knoten
                            # erreicht. Also fügen wir ein Match (=> Ausgabe) hinzu.
                            curn.addMatch(p)

    # Nachdem der trie nun gebaut ist, können die Fail-Transitionen (bzw -Knoten) ermittelt
    # werden. Dies geschieht hier.
    refreshAllFNodes([startnode], startnode)

    # Uncomment the following line to print the complete trie. But alas, beware of the cat.
    #debug_print_trie(startnode, "#### ")
    
    return startnode


def processInputChar(c, stateInAutomaton, ctr):
    curn = stateInAutomaton

    nextn = curn.getChild(c) #curn = currentNode, nextn = nextNode

    # Wenn kein regulärer Folgeknoten gefunden wird, muss die Fail-Transition
    # genommen werden. Evtl müssen weiter Fail-Transitionen genommen werden, bis
    # eine Transition mit dem aktuellen Symbol c möglich ist oder bis die Wurzel
    # erreicht wird.
    while nextn == None and curn.symbol != None:
            curn = curn.fnode
            nextn = curn.getChild(c)

    if nextn != None:
            # Es wurde ein Knoten erreicht, der nicht der Wurzelknoten ist. Das
            # kann bedeuten, dass Matches gefunden wurden. Gebe alle Matches
            # dieses knotens aus, mitsamt der Position.
            for m in nextn.matches:
                    print str(ctr - len(m) + 1) + ": " + m
            curn = nextn
    
    # Schlussendlich bewegen wir uns zum nächsten Symbol im Text vor, also muss
    # der counter inkrementiert werden.
    
    return curn
    # Want some more debug information about this stage of the Algorithm?
    # Uncomment the following line!
    #print "   " + c + ": " + str(curn.symbol)



def followHighRatedPath(curn):
    nextn = curn

    while nextn != None:
        oldn = nextn
        print(oldn.rating)
        nextn = nextn.getChildWithMaxRating()

    return oldn



#########################################################################################
# Hier beginnt die Ausführung des Skripts, wenn es in der Kommandozeile aufgerufen wird.#
# python aho.py -p ahoTest.txt
#########################################################################################
if __name__ == "__main__":
    # Erst ein wenig input parsing. Quick & dirty in diesem Fall, was hier nicht sehr 
    # schlimm ist, da wir sowieso nur immer genau 2 Paramete erwarten.
    if len(sys.argv) < 3:
            print "Usage: -p <patterns.txt>"
            sys.exit(0)

    if sys.argv[1] == "-p":
            patternfile = sys.argv[2]
    else:
            print "Usage: -p <patterns.txt>"
            sys.exit(0)

    # Wir lesen die patterns in eine liste, strippen dabei bereits alle Leerzeichen und
    # \n heraus, die am Anfang oder Ende von Zeilen stehen.
    patterns = [line.strip() for line in open(patternfile)]

    tree = buildAutomaton(patterns)



    #######################################################

    # Jetzt werden matches im Eingabetext gesucht.
    # Now use automaton to find matches.

    # Ein Zähler wird verwendet, um die Position der gefundenen Matches zu ermitteln. Hier
    # fangen wir bei 0 mit dem Zählen an - je nach Geschmack kann dies selbstverständlich
    # auf 1 geändert werden.
    ctr = 0
    # Begonnen wird an an der Wurzel.
    state = tree
    # Nun wird der trie stumpf abgelaufen. Little excitement here.
    while 1:
        c = raw_input('gimme a char!')
        state = processInputChar(c, state, ctr)
        print(state.nid, state.rating) 
        vorschlag = followHighRatedPath(state).nid
        print("Vorschlag: ", vorschlag)
        ctr += 1
