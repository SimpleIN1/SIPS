import styles from "@/components/Settings/Settings.module.scss";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";


const SortPanel = () => {
    return (
            <div className={styles.sort}>
                <p className={styles.text}>Сортировать данные за:</p>
                <Stack direction="row" spacing={0.5} padding={0.5}>
                    <Button color="secondary" variant="contained" size="small" href="!#">
                        Сегодня
                    </Button>
                    <Button color="secondary" variant="contained" size="small" href="!#">
                        24 часа
                    </Button>
                    <Button color="secondary" variant="contained" size="small" href="!#">
                        Неделя
                    </Button>
                </Stack>
        </div>
    );
};

export default SortPanel;