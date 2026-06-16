import vievi from '../assets/png/legends/vievi.png'
import clmsk from '../assets/png/legends/clmsk.png'
import aot550 from '../assets/png/legends/aot550.png'
import vlst from '../assets/png/legends/vlst.png'
import vscmo from '../assets/png/legends/vscmo.png'


export const getLegendByComposite = (composite: string) => {
    switch (composite){
        case 'vievi':{
            return vievi
        }
        case 'vindvi':{
            return vievi
        }
        case 'clmsk':{
            return clmsk
        }
        case 'clmsk2':{
            return clmsk
        }
        case 'aot550':{
            return aot550
        }

        case 'aotaps':{
            return aot550
        }

        case 'vlst':{
            return vlst
        }

        case 'vscmo':{
            return vscmo
        }
        default:{
            return aot550
            // frmsk = ?
            // clphs = ?
        }
    }
}