import React, { lazy, Suspense, useEffect } from "react";
import { Route, Routes } from "react-router-dom";
import { Loading } from "@/components/main/Loading/Loading";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { setCursorPosition } from "@/store/cursor/cursor-slice";
import Navbar from "@/components/navbar";
import { fetchComposites, fetchDates, fetchSatellites } from "@/store/tile/tile-actions";
import { EUrls } from "@/enums/EUrls";
import { ESatellite } from "@/enums/ESatellite";
import { Catalog } from "@/components/Pages/Catalog/Catalog";
import { checkAuth } from "@/store/user/user-actions";
import { NotFound } from "../Pages/NotFound";

// Lazy pages
const Header = lazy(() => import("@/components/Header"));
const Authorization = lazy(() => import("@/components/Pages/Authorization"));
const Registration = lazy(() => import("@/components/Pages/Registration"));
const RestoreAccess = lazy(() => import("@/components/Pages/RestoreAccess"));
const UserGuide = lazy(() => import("@/components/Pages/UserGuide/UserGuide"));
const AboutUs = lazy(() => import("@/components/Pages/AboutUs"));
const Map = lazy(() => import("@/components/Map/Map"));
const Profile = lazy(() => import("@/components/Pages/Profile"));
const VerifyUser = lazy(() => import("@/components/Pages/VerifyUser"));

function Main() {
  const dispatch = useAppDispatch();

  const satellite: ESatellite = useAppSelector((state) => state.tile).satellite;
  const dotdate = useAppSelector((state) => state.tile).dateTime.dotdate;
  const time: string = useAppSelector((state) => state.tile).dateTime.time;

  const isAuth: boolean = useAppSelector((state) => state.user).isAuth;

  const handleMouseMove = (event: React.MouseEvent<HTMLDivElement>) => {
    dispatch(setCursorPosition({ x: event.clientX, y: event.clientY }));
  };

  useEffect(() => {
    dispatch(fetchDates(""));
    dispatch(fetchSatellites());

    if (satellite && dotdate && time) {
      dispatch(
        fetchComposites({
          satellite: satellite as ESatellite,   // ← исправлено
          dotdate,
          dottime: time.substring(0, 2) + "-" + time.substring(2),
        })
      );
    }
  }, [dispatch, satellite, dotdate, time]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      dispatch(checkAuth());
    }
  }, [dispatch]);

  return (
    <div onMouseMove={handleMouseMove}>
      <Suspense fallback={<Loading />}>
        <Header />
      </Suspense>

      <Routes>
        <Route
          path="/"
          element={
            <Suspense fallback={<Loading />}>
              <Map />
            </Suspense>
          }
        />

        <Route
          path="/authorization"
          element={
            <Suspense fallback={<Loading />}>
              <Authorization />
            </Suspense>
          }
        />

        <Route
          path="/registration"
          element={
            <Suspense fallback={<Loading />}>
              <Registration />
            </Suspense>
          }
        />

        <Route
          path="/restore"
          element={
            <Suspense fallback={<Loading />}>
              <RestoreAccess />
            </Suspense>
          }
        />

        <Route
          path="/reset-password"
          element={
            <RestoreAccess />
          }
        />

        <Route
          path="/management"
          element={
            <Suspense fallback={<Loading />}>
              <UserGuide />
            </Suspense>
          }
        />

        <Route
          path="/home"
          element={
            <Suspense fallback={<Loading />}>
              <AboutUs />
            </Suspense>
          }
        />

        <Route
          path="/profile"
          element={
            <Suspense fallback={<Loading />}>
              {isAuth ? <Profile /> : <NotFound />}
            </Suspense>
          }
        />

        <Route
          path="/verify-user"
          element={
            <VerifyUser />
          }
        />

        <Route
          path="/catalog"
          element={
            <Suspense fallback={<Loading />}>
              {isAuth ? <Catalog /> : <NotFound />}
            </Suspense>
          }
        />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}

export default Main;