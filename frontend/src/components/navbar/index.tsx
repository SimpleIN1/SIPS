import styles from "./Navbar.module.scss";
import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { navbarLinksAuth, navbarLinksNotAuth } from "@/data/links";
import { ILink } from "@/interfaces/Ilink";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { logout } from "@/store/user/user-slice";
const AboutNavbar = () => {
  const activeLink = `${styles.navbar__link} ${styles['navbar__link--active']}`;
  const normalLink = `${styles.navbar__link}`;
  const isAuth : boolean = useAppSelector(state => state.user).isAuth
  const navbarLinks : ILink[] = isAuth ? navbarLinksAuth : navbarLinksNotAuth
  const dispatch = useAppDispatch();


  const handleLogout = () => {
    dispatch(logout())
  }

  return (
    <nav className={styles.header}>
      <div className={styles.container}>
        <Link to="/" className={styles.logo}>
          SIPS
        </Link>
        <ul className={styles.navbar}>
          {navbarLinks.map((link) => (
            <li
              key={link.id}
              className={styles.navbar__item} 
            >
              <NavLink to={link.to} className={({isActive}) => isActive ? activeLink : normalLink}>{link.title}</NavLink>
            </li>
          ))}

          {isAuth ? <button className={styles.navbar__item} onClick={handleLogout}>Выход</button> : 
          <li
            className={styles.navbar__item} 
          >
            <NavLink to={'/authorization'} className={({isActive}) => isActive ? activeLink : normalLink}>Вход</NavLink>
          </li>
          }
          



        </ul>
      </div>
    </nav>
  );
};

export default AboutNavbar;
