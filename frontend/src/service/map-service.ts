import axios, {AxiosResponse} from "axios";

export default class MapService{
    static async getRegions(url: string): Promise<AxiosResponse>{
        return axios.get(url)
    }
}