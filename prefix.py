import requests
from igraph import *
#ip = '104.154.0.0/15'
#day1='2022-8-14'
#time1='07:00'
#day2='2022-8-14'
#time2='12:00'

def RIPE(ip,day1,time1,day2,time2):
        g = Graph()
        asn_array=[]
        rutas={}
        prueba=0
        index=0
        #url = 'https://stat.ripe.net/data/ris-peerings/data.json?resource={}'.format(ip)
        #Request para obtener acceso a los datos de los peerings
        url='https://stat.ripe.net/data/ris-peerings/data.json?resource={0}&starttime={1}T{2}&endtime={3}T{4}'.format(ip,day1,time1,day2,time2)
        #url='https://stat.ripe.net/data/ris-peerings/data.json?resource={}&starttime=2012-12-21T07:00&endtime=2012-12-21T12:00'.format(ip)
        resp = requests.get(url)

        i1=len(resp.json()['data']['peerings'])
        if i1==-1:
                i1=0
        print(i1)
        print('Fin')

        #cantidad = len(resp.json()['data']['peerings'][0]['peers'][1]['routes'][0]['as_path'])
        print("Start")
        #Procesamiento de datos, para poder obtener las rutas dentro de un arreglo
        for i in range (i1):
                #if i1==0:
                #        i2=len(resp.json()['data']['peerings'][0]['peers']
                
                i2=len(resp.json()['data']['peerings'][i]['peers'])
                for j in range(i2):
                        if (len(resp.json()['data']['peerings'][i]['peers'][j]['routes'])) !=0:
                                ruta=resp.json()['data']['peerings'][i]['peers'][j]['routes'][0]['as_path']
                                rutas[index]=ruta
                                index=index+1
                                #print(ruta)
                                #asn_array.append(ruta)
                                for k in ruta:
                                        if k not in asn_array:
                                                asn_array.append(k)
                                
        #Extracción en un arreglo de todos los distintos ASN en donde se esta propagando el anuncio
        array_i=0
        g.add_vertices(len(asn_array))
        asn_paths={}
        ruta_index=[]
        #Creación de vertices del grafo a partir de la cantidad de asn's
        for i in range(len(g.vs)):
            g.vs[i]["id"]= asn_array[i]
            g.vs[i]["label"]= str(asn_array[i])

        #Creación de los edges del grafo según las rutas extraídas anteriormente
        for i in range(len(rutas)):
                for k in range(len(rutas[i])):
                        ruta_index.append(asn_array.index(rutas[i][k]))
                asn_paths[i]=ruta_index
                ruta_index=[]
        for j in range(len(asn_paths)):
            for k in range(len(asn_paths[j])-1):
                #print("ENTRA: "+str(k))
                g.add_edges([(asn_paths[j][k],asn_paths[j][k+1])])
                        
            
        
        print(rutas)
        print(g.vs[1]["id"])
        print(asn_paths)
        #Proceso para extraer el grafo como imagen, con las rutas y ans indicados anteriormente
        origen=asn_paths[0][(len(asn_paths[0])-1)]
        g.vs['color']="white"
        g.vs[origen]['color']="green"
        visual_style = {}
        out_name = "graph.png"
        # Set bbox and margin
        visual_style["bbox"] = (10000,10000)
        visual_style["margin"] = 27
        # Set vertex colours
        #visual_style["vertex_color"] = 'white'
        #print(g.vs["color"])
        #print(g.vs["label"])
        #print(g.EdgeSeq)
        #print(inspect.getmembers(g.vs))
        # Set vertex size
        visual_style["vertex_size"] = 65
        # Set vertex lable size
        visual_style["vertex_label_size"] = 22
        # Don't curve the edges
        visual_style["edge_curved"] = False
        # Set the layout
        my_layout = g.layout_lgl()
        visual_style["layout"] = my_layout
        # Plot the graph
        plot(g, out_name, **visual_style)
        #print("Enter")
        #print("Duplicate elements in given array: ");       
        #print(asn_array)
        #rutas0=rutas[1]
        #print(rutas0[0])
        #print(asn_paths[0][(len(asn_paths[0])-1)])

def Cambios(ip,day1,time1,day2,time2,asn):
    g = Graph(directed=True)
    #Request inicial para obtener los datos de los cambios de asn a través del tiempo
    url='https://stat.ripe.net/data/bgplay/data.json?resource={0}&starttime={1}T{2}&endtime={3}T{4}'.format(ip,day1,time1,day2,time2)
    resp = requests.get(url)
    rutas={}
    asn_array=[]
    index_nuevo=0
    print(resp.json()['data']['events'][0]['attrs']['path'])
    i1=len(resp.json()['data']['events'])
    #Obtención de todos los cambios ocurridos en el tiempo establecido
    for i in range(i1):
        #print(i)
        if (len(resp.json()['data']['events'][i]['attrs'])) >2:
            
            ruta=resp.json()['data']['events'][i]['attrs']['path']
            rutas[index_nuevo]=ruta
            index_nuevo=index_nuevo+1
        #Obtención de todos los asn involucrados en los cambios
        for k in ruta:
                if k not in asn_array:
                        asn_array.append(k)
    
    asn_paths={}
    ruta_index=[]
    g.add_vertices(len(asn_array))
    for i in range(len(g.vs)):
            g.vs[i]["id"]= asn_array[i]
            g.vs[i]["label"]= str(asn_array[i])

    for i in range(len(rutas)):
        for k in range(len(rutas[i])):
            ruta_index.append(asn_array.index(rutas[i][k]))
            #print(ruta_index)
            asn_paths[i]=ruta_index
        ruta_index=[]
    for j in range(len(asn_paths)):
        for k in range(len(asn_paths[j])-1):
            #print("ENTRA: "+str(k))
            g.add_edges([(asn_paths[j][k],asn_paths[j][k+1])])
            #print(str(asn_paths[j][k])+','+str(asn_paths[j][k+1]))
    #Determinación del ASN de origen
    origen=asn_paths[0][(len(asn_paths[0])-1)]
    #174 TIENE QUE SER UN INPUT
    #cambios_input=g.get_all_simple_paths(g.vs[origen], to=g.vs[asn_array.index(174)], cutoff=-1, mode='in')
    print(asn_array)
    print('este es el origen'+str(origen))
    print('este es el destino'+str(asn_array.index(int(asn))))
    #Obtención de los cambios de ruta entre el asn de origen y el asn ingresado
    cambios_input=g.get_all_simple_paths(g.vs[origen], to=g.vs[asn_array.index(int(asn))], cutoff=-1, mode='all')
    #Separación de los asn involucrados en los cambios entre los asn de interés
    asn_array_cambios=[]
    indx_n=0
    for i in range(len(cambios_input)):
        for j in range(len(cambios_input[i])):
            if asn_array[cambios_input[i][j]] not in asn_array_cambios:
                asn_array_cambios.append(asn_array[cambios_input[i][j]])
                
    #for i in range(len(asn_array_cambios)):
        #print(g.get_all_simple_paths(g.vs[origen], to=g.vs[asn_array.index(61138)], cutoff=-1, mode='all')[0][0])
    gc=Graph()
    gc.add_vertices(len(asn_array_cambios))
    print("ASNARRAY")
    print(asn_array)
    print("ASNARRAYCAMBIOS")
    print(asn_array_cambios)
    print('CAMBIOSINPUT')
    print(cambios_input)
    index_vc=0
    labels_caminos=[]
    camino=0
    #Creación de vertices del grafo a partir de los asn dentro de los cambios seleccionados
    for j in range(len(asn_array_cambios)):
        gc.vs[index_vc]['id']=asn_array_cambios[j]
        gc.vs[index_vc]['label']=str(asn_array_cambios[j])
        index_vc=index_vc+1
    #Creación de los edges del grafo según lo describen los cambios en el tiempo establecio.
    print('TOTAL CAMBIOS'+str(len(cambios_input)))
    for k in range(len(cambios_input)):
        for m in range(len(cambios_input[k])-1):
            print('actual'+str(m))
            gc.add_edges([(gc.vs[asn_array_cambios.index(asn_array[cambios_input[k][m]])],gc.vs[asn_array_cambios.index(asn_array[cambios_input[k][m+1]])])])
            labels_caminos.append(k)
            #camino=camino+1
            
    #Creación del grafo con los caminos resaltados según al cambio que corresponden
    gc.es['weight'] = labels_caminos
    gc.es['label'] = labels_caminos
    out_name=("graph1.png")
    gc.vs['color']="white"
    gc.vs[0]['color']="green"
    gc.vs[asn_array_cambios.index(int(asn))]['color']="red"
    visual_style = {}
    #out_name = "graph.png"
    # Set bbox and margin
    visual_style["bbox"] = (1000,1000)
    visual_style["margin"] = 27
    # Set vertex colours
    #visual_style["vertex_color"] = 'white'
    # Set vertex size
    visual_style["vertex_size"] = 65
    # Set vertex lable size
    visual_style["vertex_label_size"] = 22
    visual_style["edge_label_size"] = 22
    # Don't curve the edges
    visual_style["edge_curved"] = False
    # Set the layout
    my_layout = gc.layout_lgl()
    visual_style["layout"] = my_layout
    # Plot the graph
    plot(gc, out_name, **visual_style)
    print("Fin")
    
    pass


#BGPLAY()
#RIPE(ip)
#Cambios()