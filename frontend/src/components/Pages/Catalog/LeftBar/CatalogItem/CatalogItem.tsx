import s from './CatalogItem.module.scss'
import { IImage } from '@/interfaces/IImage';
import { useAppDispatch } from '@/hooks/hook';
import { downloadImage } from '@/store/catalog/catalog-actions';
import { checkAuth } from '@/store/user/user-actions';

interface Props{
    catalogitem: IImage,
}



export const CatalogItem = ({ catalogitem }: Props) => {
    const dispatch = useAppDispatch();

    const handleDownload = () => {
        dispatch(checkAuth())
        dispatch(downloadImage(catalogitem));
    }

    const removeT = (str : string) => {
        return str.replaceAll('T', ' ');
    }

    return (
        <div className={s.cataloogitem}>
            <div className={s.cataloogitemleft}>
                <div className={s.dates}>Дата: <span>{removeT(catalogitem.datetime)}</span></div>
                <div className={s.satellite}>Спутник: <span>{catalogitem.satellite}</span></div>
                <div className={s.radiometer}>Композит: <span>{catalogitem.composite}</span></div>
            </div>
            <button onClick={handleDownload}>скачать</button>
        </div>
    );
};

