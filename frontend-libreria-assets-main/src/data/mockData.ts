// src/data/mockData.ts

export interface CategoryData {
  tags: string[];
  images: Record<string, string[]>;
}

export const data: Record<string, CategoryData> = {
  Naturaleza: {
    tags: ['Bosque', 'Montana', 'Rio'],
    images: {
      Bosque:   ['bosque1.jpg', 'bosque2.jpg', 'bosque3.jpg', 'bosque4.jpg', 'bosque5.jpg'
        , 'bosque6.jpg', 'bosque7.jpg', 'bosque8.jpg', 'bosque9.jpg', 'bosque10.jpg'
      ],
      Montana: ['montana1.jpg', 'montana2.jpg', 'montana3.jpg', 'montana4.jpg', 'montana5.jpg'
        , 'montana6.jpg', 'montana7.jpg', 'montana8.jpg', 'montana9.jpg', 'montana10.jpg'
      ],
      Rio:     ['rio1.jpg', 'rio2.jpg', 'rio3.jpg', 'rio4.jpg', 'rio5.jpg', 'rio6.jpg', 'rio7.jpg'
        , 'rio8.jpg', 'rio9.jpg', 'rio10.jpg'
      ]
    }
  },
  Ciudad: {
    tags: ['Edificio', 'Calle', 'Puente'],
    images: {
      Edificio: ['edificio1.jpg', 'edificio2.jpg', 'edificio3.jpg', 'edificio4.jpg', 'edificio5.jpg', 'edificio6.jpg', 'edificio7.jpg'
        , 'edificio8.jpg', 'edificio9.jpg', 'edificio10.jpg'
      ],
      Calle:    ['calle1.jpg', 'calle2.jpg', 'calle3.jpg', 'calle4.jpg', 'calle5.jpg', 'calles6.jpg'
        , 'calle7.jpg', 'calles8.jpg', 'calles9.jpg', 'calle10.jpg'
      ],
      Puente:   ['puente1.jpg', 'puente2.jpg', 'puente3.jpg', 'puente4.jpg', 'puente5.jpg'
        , 'puente6.jpg', 'puente7.jpg', 'puente8.jpg', 'puente9.jpg', 'puente10.jpg'
      ]
    }
  },
  Animales: {
    tags: ['Perro', 'Gato', 'Pajaro'],
    images: {
      Perro:  ['perro1.jpg', 'perro2.jpg', 'perro3.jpg', 'perro4.jpg', 'perro5.jpg', 'perro6.jpg'
        , 'perro7.jpg', 'perro8.jpg', 'perro9.jpg', 'perro10.jpg'
      ],
      Gato:   ['gato1.jpg', 'gato2.jpg', 'gato3.jpg', 'gato4.jpg', 'gato5.jpg', 'gato6.jpg'
        , 'gato7.jpg', 'gato8.jpg', 'gato9.jpg', 'gato10.jpg'
      ],
      Pajaro: ['pajaro1.jpg', 'pajaro2.jpg', 'pajaro3.jpg', 'pajaro4.jpg', 'pajaro5.jpg', 'pajaro6.jpg'
        , 'pajaro7.jpg', 'pajaro8.jpg', 'pajaro9.jpg', 'pajaro10.jpg']
    }
  },
  Tecnologia: {
    tags: ['Computadora', 'Smartphone', 'Robot'],
    images: {
      Computadora: ['computadora1.jpg', 'computadora2.jpg', 'computadora3.jpg', 'computadora4.jpg'
        , 'computadora5.jpg', 'computadora6.jpg', 'computadora7.jpg', 'computadora8.jpg'
        , 'computadora9.jpg', 'computadora10.jpg'
      ],
      Smartphone:  ['smartphone1.jpg', 'smartphone2.jpg', 'smartphone3.jpg', 'smartphone4.jpg'
        , 'smartphone5.jpg', 'smartphone6.jpg', 'smartphone7.jpg', 'smartphone8.jpg'
        , 'smartphone9.jpg', 'smartphone10.jpg',
      ],
      Robot:       ['robot1.jpg', 'robot2.jpg', 'robot3.jpg', 'robot4.jpg', 'robot5.jpg'
        , 'robot6.jpg', 'robot7.jpg', 'robot8.jpg', 'robot9.jpg', 'robot10.jpg'
      ]
    }
  },
  Arte: {
    tags: ['Pintura', 'Escultura', 'Graffiti'],
    images: {
      Pintura:   ['pintura1.jpg', 'pintura2.jpg', 'pintura3.jpg', 'pintura4.jpg', 'pintura5.jpg'
        , 'pintura6.jpg', 'pintura7.jpg', 'pintura8.jpg', 'pintura9.jpg', 'pintura10.jpg'],
      Escultura: ['escultura1.jpg', 'escultura2.jpg', 'escultura3.jpg', 'escultura4.jpg', 'escultura5.jpg'
        , 'escultura6.jpg', 'escultura7.jpg', 'escultura8.jpg', 'escultura9.jpg', 'escultura10.jpg'],
      Graffiti:  ['graffiti1.jpg', 'graffiti2.jpg', 'graffiti3.jpg', 'graffiti4.jpg', 'graffiti5.jpg'
        , 'graffiti6.jpg', 'graffiti7.jpg', 'graffiti8.jpg', 'graffiti9.jpg', 'graffiti10.jpg']
    }
  },
  Comida: {
    tags: ['Fruta', 'Postre', 'Bebida'],
    images: {
      Fruta:  ['fruta1.jpg', 'fruta2.jpg', 'fruta3.jpg', 'fruta4.jpg', 'fruta5.jpg', 'fruta6.jpg'
        , 'fruta7.jpg', 'fruta8.jpg', 'fruta9.jpg', 'fruta10.jpg'],
      Postre: ['postre1.jpg', 'postre2.jpg', 'postre3.jpg', 'postre4.jpg', 'postre5.jpg', 'postre6.jpg'
        , 'postre7.jpg', 'postre8.jpg', 'postre9.jpg', 'postre10.jpg'
      ],
      Bebida: ['bebida1.jpg', 'bebida2.jpg', 'bebida3.jpg', 'bebida4.jpg', 'bebida5.jpg', 'bebida6.jpg'
        , 'bebida7.jpg', 'bebida8.jpg', 'bebida9.jpg', 'bebida10.jpg']
    }
  },
  Deportes: {
    tags: ['Futbol', 'Baloncesto', 'Ciclismo'],
    images: {
      Futbol:      ['futbol1.jpg', 'futbol2.jpg', 'futbol3.jpg', 'futbol4.jpg', 'futbol5.jpg', 'futbol6.jpg'
        , 'futbol7.jpg', 'futbol8.jpg', 'futbol9.jpg', 'futbol10.jpg'],
      Baloncesto: ['baloncesto1.jpg', 'baloncesto2.jpg', 'baloncesto3.jpg', 'baloncesto4.jpg', 'baloncesto5.jpg'
        , 'baloncesto6.jpg', 'baloncesto7.jpg', 'baloncesto8.jpg', 'baloncesto9.jpg', 'baloncesto10.jpg'
      ],
      Ciclismo:   ['ciclismo1.jpg', 'ciclismo2.jpg', 'ciclismo3.jpg', 'ciclismo4.jpg', 'ciclismo5.jpg'
        , 'ciclismo6.jpg', 'ciclismo7.jpg', 'ciclismo8.jpg', 'ciclismo9.jpg', 'ciclismo10.jpg'
      ]
    }
  },
  Viajes: {
    tags: ['Playa', 'Montana', 'Ciudad'],
    images: {
      Playa:   ['playa1.jpg', 'playa2.jpg', 'playa3.jpg', 'playa4.jpg', 'playa5.jpg', 'playa6.jpg'
        , 'playa7.jpg', 'playa8.jpg', 'playa9.jpg', 'playa10.jpg'],
      Montana: ['montana_viage1.jpg', 'montana_viage2.jpg', 'montana_viage3.jpg', 'montana_viage4.jpg'
        , 'montana_viage5.jpg', 'montana_viage6.jpg', 'montana_viage7.jpg', 'montana_viage8.jpg'
        , 'montana_viage9.jpg', 'montana_viage10.jpg'],
      Ciudad:  ['ciudad_viaje1.jpg', 'ciudad_viaje2.jpg', 'ciudad_viaje3.jpg', 'ciudad_viaje4.jpg'
        , 'ciudad_viaje5.jpg', 'ciudad_viaje6.jpg', 'ciudad_viaje7.jpg', 'ciudad_viaje8.jpg'
        , 'ciudad_viaje9.jpg', 'ciudad_viaje10.jpg']
    }
  },
  Moda: {
    tags: ['Ropa', 'Accesorios', 'Calzado'],
    images: {
      Ropa:       ['ropa1.jpg', 'ropa2.jpg', 'ropa3.jpg', 'ropa4.jpg', 'ropa5.jpg', 'ropa6.jpg'
        , 'ropa7.jpg', 'ropa8.jpg', 'ropa9.jpg', 'ropa10.jpg'],
      Accesorios: ['accesorio1.jpg', 'accesorio2.jpg', 'accesorio3.jpg', 'accesorio4.jpg', 'accesorio5.jpg'
        , 'accesorio6.jpg', 'accesorio7.jpg', 'accesorio8.jpg', 'accesorio9.jpg', 'accesorio10.jpg'],
      Calzado:    ['calzado1.jpg', 'calzado2.jpg', 'calzado3.jpg', 'calzado4.jpg', 'calzado5.jpg', 'calzado6.jpg'
        , 'calzado7.jpg', 'calzado8.jpg', 'calzado9.jpg', 'calzado10.jpg'
      ]
    }
  },
  Musica: {
    tags: ['Rock', 'Jazz', 'Classica'],
    images: {
      Rock:    ['rock1.jpg', 'rock2.jpg', 'rock3.jpg', 'rock4.jpg', 'rock5.jpg', 'rock6.jpg'
        , 'rock7.jpg', 'rock8.jpg', 'rock9.jpg', 'rock10.jpg'],
      Jazz:    ['jazz1.jpg', 'jazz2.jpg', 'jazz3.jpg', 'jazz4.jpg', 'jazz5.jpg', 'jazz6.jpg'
        , 'jazz7.jpg', 'jazz8.jpg', 'jazz9.jpg', 'jazz10.jpg'],
      Classica:['clasica1.jpg', 'clasica2.jpg', 'clasica3.jpg', 'clasica4.jpg', 'clasica5.jpg', 'clasica6.jpg'
        , 'clasica7.jpg', 'clasica8.jpg', 'clasica9.jpg', 'clasica10.jpg']
    }
  }
};
