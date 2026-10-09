/* AfyaConnect theme JS for Tryton SAO — title, logo, login hero, dark toggle, pills.
 * SPDX-License-Identifier: Apache-2.0 */
(function () {
    'use strict';

    var LOGO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none">'
        + '<rect width="48" height="48" rx="12" fill="white" fill-opacity="0.2"/>'
        + '<path d="M24 10c-6.6 0-12 5.4-12 12 0 8.4 12 16 12 16s12-7.6 12-16c0-6.6-5.4-12-12-12z" fill="white"/>'
        + '<circle cx="24" cy="22" r="5" fill="#0d9488"/>'
        + '<path d="M14 34h20" stroke="white" stroke-width="2.5" stroke-linecap="round"/></svg>';

    function applyThemeAttr() {
        document.documentElement.setAttribute('theme', 'afyaconnect');
    }

    function darkEnabled() {
        try {
            var saved = localStorage.getItem('afya-dark');
            if (saved === '1') { return true; }
            if (saved === '0') { return false; }
        } catch (e) { /* private mode */ }
        return window.matchMedia
            && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    function applyDark() {
        document.documentElement.toggleAttribute
            ? document.documentElement.toggleAttribute('data-afya-dark', darkEnabled())
            : document.documentElement.setAttribute('data-afya-dark', darkEnabled() ? '1' : '0');
        if (!darkEnabled()) { document.documentElement.setAttribute('data-afya-dark', '0'); }
        else { document.documentElement.setAttribute('data-afya-dark', '1'); }
    }

    function toggleDark() {
        var on = document.documentElement.getAttribute('data-afya-dark') !== '1';
        try { localStorage.setItem('afya-dark', on ? '1' : '0'); } catch (e) {}
        document.documentElement.setAttribute('data-afya-dark', on ? '1' : '0');
    }

    function addDarkToggle() {
        if (document.getElementById('afya-dark-toggle')) { return; }
        var btn = document.createElement('button');
        btn.id = 'afya-dark-toggle';
        btn.title = 'Toggle dark mode';
        btn.setAttribute('aria-label', 'Toggle dark mode');
        btn.style.cssText = 'position:fixed;bottom:16px;right:16px;z-index:9999;'
            + 'width:44px;height:44px;border-radius:50%;border:1px solid #e2e8f0;'
            + 'background:#fff;box-shadow:0 4px 16px rgba(15,23,42,.18);cursor:pointer;font-size:18px;';
        btn.textContent = '◐';
        btn.addEventListener('click', toggleDark);
        document.body.appendChild(btn);
    }

    function brandLogin(dialog) {
        if (!dialog || !dialog.body || dialog.body.hasClass('afya-branded')) { return; }
        dialog.body.addClass('afya-branded');
        var hero = jQuery('<div/>', { 'class': 'afya-login-hero' });
        hero.append(
            jQuery('<div/>', { 'class': 'afya-login-logo' }).html(LOGO),
            jQuery('<h2/>', { 'class': 'afya-login-title' }).text('AfyaConnect'),
            jQuery('<p/>', { 'class': 'afya-login-tagline' })
                .text('GNU Health · AI-assisted triage · Citizen access'));
        var form = jQuery('<div/>', { 'class': 'afya-login-form' });
        dialog.body.children().appendTo(form);
        var langs = jQuery('<div/>', { 'class': 'afya-login-langs', role: 'group' })
            .append(jQuery('<button type="button">English</button>')
                .attr('aria-pressed', 'true'))
            .append(jQuery('<button type="button">Hausa</button>'))
            .append(jQuery('<button type="button">Fulfulde</button>'));
        langs.on('click', 'button', function () {
            langs.find('button').attr('aria-pressed', 'false');
            jQuery(this).attr('aria-pressed', 'true');
        });
        form.append(langs);
        dialog.body.empty().append(hero, form);
    }

    function paintTriagePills() {
        document.querySelectorAll('td').forEach(function (td) {
            var v = (td.textContent || '').trim().toLowerCase();
            if (['green', 'yellow', 'red', 'emergency'].indexOf(v) === -1) { return; }
            if (td.querySelector('.afya-pill')) { return; }
            var pill = document.createElement('span');
            pill.className = 'afya-pill afya-pill-' + v;
            pill.textContent = v.toUpperCase();
            td.textContent = '';
            td.appendChild(pill);
        });
    }

    applyThemeAttr();
    applyDark();
    document.addEventListener('DOMContentLoaded', function () {
        addDarkToggle();
        setInterval(paintTriagePills, 1500);
    });

    if (typeof Sao !== 'undefined') {
        Sao.config.title = 'AfyaConnect';
        Sao.config.graph_color = '#0d9488';
        if (Sao.Session && Sao.Session.login_dialog) {
            var orig = Sao.Session.login_dialog;
            Sao.Session.login_dialog = function () {
                var d = orig();
                d.modal.addClass('afya-login-modal');
                setTimeout(function () { brandLogin(d); }, 0);
                return d;
            };
        }
    }

    window.AfyaTheme = { toggleDark: toggleDark };
})();
