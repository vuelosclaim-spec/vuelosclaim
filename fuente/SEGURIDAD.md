# Seguridad y credenciales — auditoría del 23-10-2026

Ningún valor secreto aparece en este documento.

## Método

- `gitleaks` 8.21.2 sobre todo el historial (`--all`: ramas `main`, `mejora-vuelosclaim-2026`, `auditoria-final-2026` y remotas) y sobre los archivos actuales.
- Búsqueda adicional por patrones en el historial: tokens de Netlify (`nfp_`), GitHub (`ghp_`, `gho_`…), Google (`AIza`), claves privadas, `NETLIFY_AUTH_TOKEN` y asignaciones `api_key`, `secret`, `password` o `token`.
- Revisión de nombres de archivo sensibles en el historial (`.env`, `.pem`, `.key`, `netlify.toml`…), de la URL del remoto git y del flujo de CI.

## Resultado en el repositorio

| Ámbito | Resultado |
| --- | --- |
| Código fuente | Sin secretos |
| Historial git (26 commits, todas las ramas) | Sin secretos |
| Configuración | Sin `.env` ni `netlify.toml`. El remoto `origin` no lleva credenciales en la URL |
| CI (`.github/workflows/validar.yml`) | No usa `secrets.*` ni tokens: solo compila y pasa las pruebas |
| Documentación | Solo menciona que existe un token de Netlify, sin su valor |
| `fuente/src_static/indexnow.key` | **No es un secreto.** IndexNow exige publicar esa clave en la web para verificar el dominio |
| Identificadores públicos (GA4 `G-6JRCZVTNDG`, AdSense `ca-pub-…`, Travelpayouts) | Son públicos por diseño, porque van en el HTML |

## Fuera del repositorio

### Token personal de Netlify

- En Netlify → User settings → Applications → Personal access tokens hay **un token, llamado «claude»**. Se creó el 19-10 y caduca solo el **26-10-2026**.
- **Dependencias:** ninguna.
  - El sitio se sirve desde GitHub Pages: la cabecera `server` es GitHub.com y el CNAME es `vuelosclaim.eu`.
  - Ni el CI ni los scripts de despliegue lo usan.
  - worldcupdle y taupe-kulfi se publicaron por última vez en junio, antes de crear el token.
- El valor solo estaba en un registro interno de la sesión de trabajo, que ya se ha borrado de ese registro. Nunca estuvo en git.
- **Resuelto:** el propietario lo borró el 25-10-2026. Comprobado en Netlify: en «Personal access tokens» ya no hay ningún token.

**Cómo revocarlo:**
1. Entra en app.netlify.com con salvalloris@gmail.com.
2. Haz clic en tu avatar → **User settings** → **Applications**.
3. En **Personal access tokens**, en la fila «claude», pulsa **Options** → **Delete** (o **Revoke**) y confirma.

### Copia antigua del sitio en Netlify — problema comprobado (resuelto el 23-10-2026)

El proyecto de Netlify `vuelosclaim` (publicado por última vez el 20-10) estaba en línea en `vuelosclaim.netlify.app`, con la versión anterior a las mejoras:

- Carga Google Analytics (`G-6JRCZVTNDG`) y Travelpayouts **sin esperar al consentimiento**.
- Mantiene el campo **IBAN** en la carta.
- Envía datos a la misma propiedad de GA4, así que mezcla visitas de esa copia con las de vuelosclaim.eu.
- Tiene el canonical hacia vuelosclaim.eu, así que el riesgo SEO es bajo, pero el contenido jurídico está desactualizado.

**Resuelto:** el propietario borró el proyecto el 23-10-2026. Comprobado: `vuelosclaim.netlify.app` responde 404, vuelosclaim.eu responde 200 desde GitHub Pages y worldcupdle y taupe-kulfi siguen intactos. Procedimiento seguido: borrar el proyecto `vuelosclaim` de Netlify, en Project configuration → Configuration → Danger zone → Delete project. No afecta a vuelosclaim.eu, que está en GitHub Pages.

No toques worldcupdle ni taupe-kulfi.

## Otras recomendaciones

- Activar la verificación en dos pasos en Netlify y en la cuenta de GitHub `vuelosclaim-spec`, si no lo está.
- En GitHub, activar **Secret scanning** y **Push protection** (Settings → Code security). Son gratuitas en repositorios públicos.
