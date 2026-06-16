import { configureStore } from '@reduxjs/toolkit';

// редьюсеры
import mapReducer    from './map/map-slice';
import cursorReducer  from './cursor/cursor-slice';
import rulerReducer   from './ruler/ruler-slice';
import tileReducer    from './tile/tile-slice';
import userSlice      from './user/user-slice';
import catalogSlice   from './catalog/catalog-slice';

export const store = configureStore({
  reducer: {
    map:     mapReducer,
    cursor:  cursorReducer,
    ruler:   rulerReducer,
    tile:    tileReducer,
    user:    userSlice,       // лучше писать единообразно (userSlice → user)
    catalog: catalogSlice,
  },

  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,   // отключаем, если есть non-serializable данные (часто Date, Map, Set и т.д.)
      // thunk: true               ← это значение по умолчанию, можно не писать
    }),
});

// Типы (самый рекомендуемый и современный способ в 2024–2026)
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;