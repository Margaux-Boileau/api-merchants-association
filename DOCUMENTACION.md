# Proyecto de Comunicación de Asociación de Comerciantes de Sants Creu Coberta

## Descripción

La idea principal del proyecto es crear una app con la que los integrantes de la asociación de comerciantes de Sants Creu Coberta puedan comunicarse entre ellos. Para ello se ha realizado una app multiplataforma con un sistema de foros donde los usuarios pueden hacer publicaciones en los diferentes foros que hay en la aplicación para informar y comunicarse con el resto de integrantes de la asociación. La app tiene implementadas notificaciones push para así informar a los usuarios de las nuevas publicaciones.

La app también tiene implementado un sistema de gestión de usuarios para que el dueño de la tienda pueda registrar a sus empleados para que ellos también tengan acceso a la app y a los foros.

## Arquitectura

La aplicación está desarrollada en Flutter, la api rest que us en Django y la base de datos en Sqlite. La api y la bdd están en una ec2 de AWS.  
[Link al diagrama de arquitectura](https://drive.google.com/file/d/19VVdUpMCnq2gYldLzm2TB8bwS91aUMgP/view?usp=sharing)

## Diseño BDD

[Link al diagrama de Entidad-Relación de la BDD](https://drive.google.com/file/d/1iozF23-OY7YI1SFstdp_axlB5Foo7eTm/view?usp=sharing)

## Link al documento inicial

[Link al Documento Inicial](https://docs.google.com/document/d/1J5Xa9AiHJPNv99BRgMHWtEBszLd5BKL1/edit?usp=sharing&ouid=115107902726213597193&rtpof=true&sd=true)

## Reflexión y Conclusiones

Creemos que el resultado del proyecto ha sido muy bueno. El proyecto empezó con un
cliente con una propuesta un poco abstracta, sin mucha definición, pero creemos que hemos
sabido interpretar bien las necesidades del cliente y las hemos plasmado eficazmente en nuestro
proyecto.

A nivel de programación en este proyecto
hemos obtenido buenos resultados y hemos aprendido cosas tanto a nivel de
frontend(notificaciones push, implementación de audios, traducciones...) como a nivel de
backend(django en general, firebase messaging, web tokens...).