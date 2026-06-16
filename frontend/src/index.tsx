import Main from "@/components/main/main";
import {BrowserRouter} from "react-router-dom";
import {Provider} from "react-redux";
import {store} from "@/store";
import {createRoot} from "react-dom/client";

const container = document.getElementById("root");
const root = createRoot(container)
root.render(
    <BrowserRouter>
        <Provider store={store}>
            <Main/>
        </Provider>
    </BrowserRouter>
);


