#include "helper.h"
#include <iostream>
#include <QDebug>
#include <QProcess>
#include <kdebug.h>

ActionReply Helper::save(const QVariantMap &args)
{
    ActionReply reply;

    int ret = 0; // error code
    bool osdriver = args.value("osdriver").toBool();
    bool vendordriver = args.value("vendordriver").toBool();
    bool genericdriver = args.value("genericdriver").toBool();

    QStringList cliOsArgs;
    QStringList cliVendorArgs;
    QStringList cliGenericArgs;
    cliOsArgs << "up" << "os";
    cliVendorArgs << "up" << "vendor";
    cliGenericArgs << "up" << "generic";
    QString program = "/usr/libexec/panda-helper";

    QProcess *p = new QProcess(this);

    if (osdriver){
        p->start(program, cliOsArgs);
        p->waitForFinished();
        QByteArray currentDriver = p->readAllStandardOutput();
        QString osOutput = QString(currentDriver).trimmed();
        qDebug() << "OS: " << osOutput;
    } else if (vendordriver) {
        p->start(program, cliVendorArgs);
        p->waitForFinished();
        QByteArray currentDriver = p->readAllStandardOutput();
        QString vendorOutput = QString(currentDriver).trimmed();
        qDebug() << "Vendor: " << vendorOutput;
    } else if (genericdriver) {
        p->start(program, cliGenericArgs);
        p->waitForFinished();
        QByteArray currentDriver = p->readAllStandardOutput();
        QString genericOutput = QString(currentDriver).trimmed();
        qDebug() << "Generic: " << genericOutput;
    }

    /* Just an helperarg example for type string
    QString tempBackgroundConfigName = args.value("tempbackgroundrcfile").toString(); */

    if (ret == 0) {
      return ActionReply::SuccessReply;
    } else {
      reply = ActionReply::HelperErrorReply;
      reply.setErrorCode(5);

      return reply;
    }
}


KDE4_AUTH_HELPER_MAIN("org.kde.kcontrol.kcmpanda", Helper)
