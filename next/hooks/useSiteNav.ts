"use client";

import { useEffect } from "react";

/** Mirrors js/site.js nav dropdown + header scroll behavior for shared site chrome. */
export function useSiteNav() {
  useEffect(() => {
    document.querySelectorAll(".nav-services, .nav-about").forEach((nav) => {
      const btn = nav.querySelector(".nav-svc-btn");
      let closeTimer: ReturnType<typeof setTimeout>;

      const open = () => {
        clearTimeout(closeTimer);
        nav.classList.add("is-open");
      };

      const scheduleClose = () => {
        closeTimer = setTimeout(() => nav.classList.remove("is-open"), 160);
      };

      nav.addEventListener("mouseenter", open);
      nav.addEventListener("mouseleave", scheduleClose);
      nav.addEventListener("focusin", open);
      nav.addEventListener("focusout", (e) => {
        const related = (e as FocusEvent).relatedTarget as Node | null;
        if (!related || !nav.contains(related)) scheduleClose();
      });

      const onClick = (e: Event) => {
        if (window.matchMedia("(max-width: 900px)").matches) return;
        e.preventDefault();
        nav.classList.toggle("is-open");
      };
      btn?.addEventListener("click", onClick);
    });

    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        document
          .querySelectorAll(".nav-services.is-open, .nav-about.is-open")
          .forEach((n) => n.classList.remove("is-open"));
      }
    };

    const onDocClick = (e: MouseEvent) => {
      const target = e.target as Element;
      if (!target.closest(".nav-services") && !target.closest(".nav-about")) {
        document
          .querySelectorAll(".nav-services.is-open, .nav-about.is-open")
          .forEach((n) => n.classList.remove("is-open"));
      }
    };

    document.addEventListener("keydown", onKeyDown);
    document.addEventListener("click", onDocClick);

    const hdr = document.getElementById("header");
    const updateHeader = () => {
      if (!hdr) return;
      const scrolled = window.scrollY > 20;
      hdr.classList.toggle("solid", scrolled);
      hdr.classList.toggle("top", !scrolled);
    };
    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });

    const hamburger = document.getElementById("hamburger");
    const mobileMenu = document.getElementById("mobileMenu");
    const onHamburger = () => mobileMenu?.classList.toggle("open");
    hamburger?.addEventListener("click", onHamburger);

    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.removeEventListener("click", onDocClick);
      window.removeEventListener("scroll", updateHeader);
      hamburger?.removeEventListener("click", onHamburger);
    };
  }, []);
}
